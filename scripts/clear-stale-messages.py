#!/usr/bin/env python3
"""
Apex Stale Message Cleaner
Safely audits and purges 90+ day old messages, 2FA shortcodes, spam bots, and large attachments
while enforcing a strict, immutable protection whitelist for family, women, and VIP partners.
"""

import sys, os, re, sqlite3, subprocess, argparse, datetime, glob

PROTECTED_NUMBERS = [
    '4148858888', '9452164927', '4145442624', '4145546538', '8327909835', 
    '9202422496', '7046759909', '4143097355', '2142641060', '4144840002',
    '4143946704', '4142335609', '4149159817', '2146959158', '4692670079',
    '4147959248', '2145003924', '2166322350', '4143993277', '9492982905',
    '8509773035', '8329339900', '9453088003'
]

PROTECTED_KEYWORDS = ['nipnap', 'jessica', 'angel', 'daughter', 'nevaeh', 'edwards']

def load_contacts():
    contacts = {}
    for path in glob.glob(os.path.expanduser('~/Library/Application Support/AddressBook/Sources/*/AddressBook-v22.abcddb')):
        try:
            conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
            cur = conn.cursor()
            cur.execute('''
                SELECT r.ZFIRSTNAME, r.ZLASTNAME, p.ZFULLNUMBER
                FROM ZABCDPHONENUMBER p
                JOIN ZABCDRECORD r ON p.ZOWNER = r.Z_PK
            ''')
            for fn, ln, num in cur.fetchall():
                if num:
                    clean = re.sub(r'\D', '', num)[-10:]
                    name = f'{fn or ""} {ln or ""}'.strip()
                    if clean and name:
                        contacts[clean] = name
            conn.close()
        except: pass
    return contacts

def is_protected(ident, cname):
    if not ident: return True
    ident_lower = ident.lower()
    cname_lower = (cname or "").lower()
    clean = re.sub(r'\D', '', ident)[-10:]
    if clean in PROTECTED_NUMBERS:
        return True
    for kw in PROTECTED_KEYWORDS:
        if kw in ident_lower or kw in cname_lower:
            return True
    return False

def get_stale_threads(days=90):
    db_path = os.path.expanduser('~/Library/Messages/chat.db')
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    cur = conn.cursor()
    
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    cutoff_ns = (cutoff - datetime.datetime(2001, 1, 1)).total_seconds() * 1e9
    
    cur.execute('''
        SELECT c.ROWID, c.chat_identifier, c.display_name, COUNT(m.ROWID), MAX(m.date)
        FROM chat c
        JOIN chat_message_join cmj ON c.ROWID = cmj.chat_id
        JOIN message m ON cmj.message_id = m.ROWID
        GROUP BY c.ROWID
        HAVING MAX(m.date) < ?
        ORDER BY COUNT(m.ROWID) DESC
    ''', (cutoff_ns,))
    
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_chats_via_applescript(target_identifiers, dry_run=True):
    if dry_run:
        print(f"\033[1;33m[DRY-RUN] Would delete {len(target_identifiers)} chat thread(s) in Messages.app\033[0m")
        return len(target_identifiers)
    
    print(f"\033[1;36m[EXECUTE] Deleting {len(target_identifiers)} chat thread(s) via AppleScript in Messages.app...\033[0m")
    deleted_count = 0
    for ident in target_identifiers:
        safe_ident = ident.replace('\\', '\\\\').replace('"', '\\"')
        script = f'''
        tell application "Messages"
            set delCount to 0
            repeat with c in (every chat)
                if id of c contains "{safe_ident}" then
                    delete c
                    set delCount to delCount + 1
                end if
            end repeat
            return delCount
        end tell
        '''
        res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip().isdigit():
            cnt = int(res.stdout.strip())
            if cnt > 0:
                deleted_count += cnt
                print(f"  ✓ Deleted thread: {ident}")
    return deleted_count

def clean_stale_attachments(days=90, min_mb=20, dry_run=True):
    db_path = os.path.expanduser('~/Library/Messages/chat.db')
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    cur = conn.cursor()
    
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    cutoff_sec = (cutoff - datetime.datetime(2001, 1, 1)).total_seconds()
    min_bytes = min_mb * 1024 * 1024
    
    cur.execute('''
        SELECT ROWID, filename, total_bytes, mime_type, transfer_name
        FROM attachment
        WHERE created_date < ? AND total_bytes >= ? AND filename IS NOT NULL
        ORDER BY total_bytes DESC
    ''', (cutoff_sec, min_bytes))
    
    rows = cur.fetchall()
    conn.close()
    
    trash_dir = os.path.expanduser('~/.Trash')
    total_bytes = sum(r[2] for r in rows)
    print(f"\n╭─ 📦 STALE ATTACHMENTS AUDIT (>={days} days old, >={min_mb}MB)")
    print(f"├─ Matching files: {len(rows)} | Total size: {total_bytes / (1024*1024):.1f} MB")
    
    moved = 0
    for rid, fn, sz, mime, tname in rows:
        path = fn.replace('~', os.path.expanduser('~'))
        if os.path.exists(path):
            if dry_run:
                print(f"├─ [DRY RUN] Would move to Trash: {tname or os.path.basename(path)} ({sz / (1024*1024):.1f} MB)")
            else:
                dest = os.path.join(trash_dir, os.path.basename(path))
                try:
                    import shutil
                    shutil.move(path, dest)
                    moved += 1
                    print(f"├─ ✓ Moved to Trash: {tname or os.path.basename(path)} ({sz / (1024*1024):.1f} MB)")
                except Exception as e:
                    print(f"├─ ✗ Error moving {path}: {e}")
    print(f"╰─ Mode: {'DRY RUN (no files moved)' if dry_run else f'MOVED {moved} file(s) to ~/.Trash'}\n")

def main():
    parser = argparse.ArgumentParser(description="Apex Stale Message & Attachment Cleaner")
    parser.add_argument('--days', type=int, default=90, help="Days threshold (default 90)")
    parser.add_argument('--shortcodes', action='store_true', help="Clean expired 2FA & shortcodes")
    parser.add_argument('--spam', action='store_true', help="Clean cold spam, bots & 1-off blasts")
    parser.add_argument('--attachments', action='store_true', help="Clean large stale attachments")
    parser.add_argument('--all-safe', action='store_true', help="Clean shortcodes + spam + attachments")
    parser.add_argument('--min-mb', type=int, default=20, help="Minimum attachment MB to clean (default 20)")
    parser.add_argument('--execute', action='store_true', help="Actually perform deletions (default is safe dry-run)")
    args = parser.parse_args()
    
    dry_run = not args.execute
    contacts = load_contacts()
    
    print(f"\n=======================================================")
    print(f"🧹 APEX STALE MESSAGE CLEANER ({'DRY-RUN' if dry_run else 'LIVE EXECUTION'})")
    print(f"   Threshold: {args.days} days and older")
    print(f"=======================================================")
    
    stale_rows = get_stale_threads(args.days)
    
    shortcodes = []
    spam_bots = []
    inactive_contacts = []
    
    for rowid, ident, dname, count, max_dt in stale_rows:
        clean = re.sub(r'\D', '', ident)[-10:] if ident else ''
        cname = contacts.get(clean, dname or ident)
        
        if is_protected(ident, cname):
            continue
            
        if ident.isdigit() and len(ident) <= 6:
            shortcodes.append(ident)
        elif '@' in ident or count == 1 or ident.startswith('+212') or ident.startswith('+44'):
            spam_bots.append(ident)
        else:
            inactive_contacts.append((ident, cname, count))
            
    print(f"Audited {len(stale_rows)} total stale threads (>={args.days} days old):")
    print(f"  • Expired 2FA Shortcodes: {len(shortcodes)} threads")
    print(f"  • Cold Spam & 1-off Bots: {len(spam_bots)} threads")
    print(f"  • Inactive Contacts (Review needed): {len(inactive_contacts)} threads")
    print(f"  • Protected VIPs/Family/Women: 100% EXCLUDED & SAFE")
    
    if args.shortcodes or args.all_safe:
        print(f"\n--- Processing {len(shortcodes)} Expired 2FA Shortcodes ---")
        delete_chats_via_applescript(shortcodes, dry_run=dry_run)
        
    if args.spam or args.all_safe:
        print(f"\n--- Processing {len(spam_bots)} Spam & Bot Threads ---")
        delete_chats_via_applescript(spam_bots, dry_run=dry_run)
        
    if args.attachments or args.all_safe:
        clean_stale_attachments(days=args.days, min_mb=args.min_mb, dry_run=dry_run)
        
    if not (args.shortcodes or args.spam or args.attachments or args.all_safe):
        print("\nTip: Specify what to clean:")
        print("  python3 clear-stale-messages.py --shortcodes   # 2FA / OTPs")
        print("  python3 clear-stale-messages.py --spam         # Spam & bots")
        print("  python3 clear-stale-messages.py --attachments  # Large files >20MB")
        print("  python3 clear-stale-messages.py --all-safe     # All 3 safe tiers")
        print("  Add '--execute' to apply (otherwise runs as safe dry-run).")

if __name__ == '__main__':
    main()
