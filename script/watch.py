import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import xml.etree.ElementTree as ET

WATCH_DIR = os.environ.get('WATCH_DIR', '/app/media')

class DescriptionToNFOHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            basename = os.path.splitext(event.src_path)[0]
            description_file = f"{basename}.description"
            nfo_file = f"{basename}.nfo"

            if os.path.exists(description_file) and os.path.exists(nfo_file):
                try:
                    print(f"Found matching files: {description_file} and {nfo_file}", file=sys.stderr)
                    time.sleep(5) 

                    # Read description
                    with open(description_file, 'r', encoding='utf-8') as f:
                        description = f.read().strip().replace('\n', '  \n')

                    # Read and parse NFO
                    tree = ET.parse(nfo_file)
                    root = tree.getroot()

                    # Find or create the <plot> field (common in Kodi/Jellyfin NFO)
                    plot = root.find('plot')
                    if plot is None:
                        plot = ET.SubElement(root, 'plot')
                    plot.text = description

                    # Overwrite NFO
                    tree.write(nfo_file, encoding='utf-8', xml_declaration=True)

                    # Delete description file
                    os.remove(description_file)
                    print(f"Merged description into {nfo_file} and deleted {description_file}.", file=sys.stderr)
                except Exception as e:
                    print(e, file=sys.stderr)


if __name__ == "__main__":
    event_handler = DescriptionToNFOHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"Watching directory: {WATCH_DIR}", file=sys.stderr)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
