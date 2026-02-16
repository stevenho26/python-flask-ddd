import sys
import os
import struct
import gzip

# Force UTF-8 for stdout/stderr to avoid Windows console encoding errors
sys.stdout.reconfigure(encoding='utf-8')

# Add project root to sys.path so we can import app modules
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from app.main import create_app
from infrastructure.database import db
from infrastructure.repository.dictionary_models import DictionaryDTO

def import_stardict(dict_dir, dict_name):
    print(f"Starting import for {dict_name}...")
    
    # Construct file paths
    # Note: .ifo is optional for our logic as we assume default format, 
    # but good to have.
    dict_path = os.path.join(dict_dir, f"{dict_name}.dict.dz")
    idx_path = os.path.join(dict_dir, f"{dict_name}.idx")

    if not os.path.exists(idx_path):
        print(f"Error: Index file not found at {idx_path}")
        return
    if not os.path.exists(dict_path):
        print(f"Error: Dict file not found at {dict_path}")
        return

    # Check if data might already exist
    try:
        if DictionaryDTO.query.count() > 0:
            print("Detected existing dictionary data in MySQL.")
            response = input("Database is not empty. Do you want to CLEAR all data and re-import? (y/n): ")
            if response.lower() == 'y':
                print("Clearing existing data...")
                db.session.query(DictionaryDTO).delete()
                db.session.commit()
                print("Table cleared.")
            else:
                print("Skipping import to avoid duplicates.")
                return
    except Exception as e:
        print(f"Checking table failed (will attempt to create/import anyway): {e}")

    print("Loading dictionary content into memory...")
    
    # Read .dict.dz content into memory (gunzip)
    try:
        with gzip.open(dict_path, 'rb') as f:
            dict_content = f.read()
    except Exception as e:
        print(f"Error reading .dict.dz file: {e}")
        return

    print(f"Dictionary content loaded. Size: {len(dict_content)} bytes.")

    # Process .idx file
    entries = []
    print("Processing index file...")
    
    with open(idx_path, 'rb') as f:
        idx_content = f.read()
    
    i = 0
    count = 0
    total_len = len(idx_content)
    
    # We assume 32-bit offset (default for most StarDict unless 64-bit flag is set)
    # File size of .idx is 478200 bytes.
    
    while i < total_len:
        # 1. Read word string (null-terminated)
        null_pos = idx_content.find(b'\0', i)
        if null_pos == -1:
            break
            
        word_bytes = idx_content[i:null_pos]
        word = word_bytes.decode('utf-8', errors='ignore')
        
        # Move past null byte
        i = null_pos + 1
        
        # 2. Read offset (4 bytes) and size (4 bytes) - Big Endian (>II)
        if i + 8 > total_len:
            break
            
        offset, size = struct.unpack('>II', idx_content[i:i+8])
        i += 8
        
        # 3. Extract definition
        if offset + size <= len(dict_content):
            def_bytes = dict_content[offset : offset + size]
            definition = def_bytes.decode('utf-8', errors='replace')
            
            # Create DTO
            entry = DictionaryDTO(word=word, definition=definition)
            entries.append(entry)
            count += 1
        else:
            print(f"Warning: Offset out of bounds for word '{word}'")
        
        if count % 5000 == 0:
            print(f"Parsed {count} entries...")
    
    print(f"Parsing complete. Total entries: {count}")
    
    if count > 0:
        print("Saving to database (this may take a moment)...")
        try:
            # Construct chunks to avoid memory issues with too large transaction
            chunk_size = 2000
            for k in range(0, len(entries), chunk_size):
                chunk = entries[k : k + chunk_size]
                db.session.bulk_save_objects(chunk)
                db.session.commit()
                print(f"Saved {min(k + chunk_size, len(entries))}/{len(entries)}")
                
            print("Dictionary imported successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to database: {e}")
    else:
        print("No entries found to import.")

if __name__ == "__main__":
    print("Initializing app context...")
    app = create_app()
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        import_stardict(os.path.join(project_root, 'vi-vi'), 'star_vietviet')
