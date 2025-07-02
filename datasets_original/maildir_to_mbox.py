import os
import sys
import argparse
import mailbox
import email

#Scan for email headers in the first chunk of a file.
def detect_email_file(path, max_bytes=2048):

    try:
        with open(path, 'rb') as f:
            head = f.read(max_bytes)
    except OSError:
        return False

    for hdr in (b"From:", b"To:", b"Subject:", b"Return-Path:"):
        if hdr in head:
            return True
    return False

# Walk the source directory, parse every email file, and add it to an mbox.
def merge_maildir(source_dir, dest_mbox):
    mbox = mailbox.mbox(dest_mbox)
    mbox.lock()
    count_added = 0
    count_skipped = 0

    for dirpath, _, filenames in os.walk(source_dir):
        for name in filenames:
            path = os.path.join(dirpath, name)

            # Skip non-files or empty files
            if not os.path.isfile(path) or os.path.getsize(path) == 0:
                count_skipped += 1
                continue

            # Skip if it is not an email
            if not detect_email_file(path):
                count_skipped += 1
                print(f"Skipping: not an email → {path}", file=sys.stderr)
                continue

            # Parse and add to mbox
            try:
                with open(path, 'rb') as f:
                    message = email.message_from_binary_file(f)
                mbox.add(message)
                count_added += 1
            except Exception as e:
                count_skipped += 1
                print(f"Error parsing {path}: {e}", file=sys.stderr)

    mbox.flush()
    mbox.unlock()
    return count_added, count_skipped

def main():
    parser = argparse.ArgumentParser(
        description="Merge a Maildir-style tree into one mbox file."
    )
    parser.add_argument("source_dir",
                        help="Path to your maildir folder")
    parser.add_argument("dest_mbox",
                        help="Output mbox file path")
    args = parser.parse_args()

    print(f"Scanning {args.source_dir!r} …")
    added, skipped = merge_maildir(args.source_dir, args.dest_mbox)
    print(f"Done. Added {added} messages, skipped {skipped} files.")
    print(f"Result: {args.dest_mbox!r}")

if __name__ == "__main__":
    main()