import os
import requests
import shutil

current_paths = {}
user_pages = {}

def get_file_tree(path="C:\\", page=1, items_per_page=25):
    try:
        if not os.path.exists(path):
            return "Path does not exist"
        
        all_items = []
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                all_items.append(f"📁 {item}/")
            else:
                size = get_file_size(item_path)
                all_items.append(f"📄 {item} ({size})")
        
        total_items = len(all_items)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        
        if total_items == 0:
            return f"📂 {path}\n└── (empty folder)"
        
        page = max(1, min(page, total_pages))
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        page_items = all_items[start_idx:end_idx]
        
        tree_lines = []
        tree_lines.append(f"📂 {path}")
        
        if total_pages > 1:
            tree_lines.append(f"📄 Page {page}/{total_pages} | Items {start_idx + 1}-{end_idx} of {total_items}")
        
        for i, item in enumerate(page_items):
            if i == len(page_items) - 1:
                tree_lines.append(f"└── {item}")
            else:
                tree_lines.append(f"├── {item}")
        
        if total_pages > 1:
            nav_info = []
            if page > 1:
                nav_info.append(f"!page {page - 1} (prev)")
            if page < total_pages:
                nav_info.append(f"!page {page + 1} (next)")
            if nav_info:
                tree_lines.append("")
                tree_lines.append("🔸 " + " | ".join(nav_info))
        
        result = "\n".join(tree_lines)
        
        if len(result) > 1900:
            return get_file_tree(path, page, max(10, items_per_page - 5))
        
        return result
        
    except PermissionError:
        return f"❌ Access denied to {path}"
    except Exception as e:
        return f"❌ Error: {e}"

def get_page(user_id, page_number):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        user_pages[user_id] = page_number
        return get_file_tree(current_path, page_number)
    except Exception as e:
        return f"❌ Page error: {e}"

def navigate_to(user_id, folder_name):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        
        if folder_name == "..":
            new_path = os.path.dirname(current_path)
        else:
            new_path = os.path.join(current_path, folder_name)
        
        if os.path.exists(new_path) and os.path.isdir(new_path):
            current_paths[user_id] = new_path
            user_pages[user_id] = 1
            return get_file_tree(new_path, 1)
        else:
            return f"❌ Folder '{folder_name}' not found"
    except Exception as e:
        return f"❌ Navigation error: {e}"

def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    except:
        return "Unknown"

def delete_file(user_id, filename):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        file_path = os.path.join(current_path, filename)
        
        if not os.path.exists(file_path):
            return f"❌ '{filename}' not found"
        
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
            return f"✅ Folder '{filename}' deleted"
        else:
            os.remove(file_path)
            return f"✅ File '{filename}' deleted"
    except PermissionError:
        return f"❌ Access denied - cannot delete '{filename}'"
    except Exception as e:
        return f"❌ Delete error: {e}"

def upload_to_gofile(file_path):
    try:
        with open(file_path, 'rb') as file:
            response = requests.post('https://store1.gofile.io/uploadFile', 
                                   files={'file': file})
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ok':
                return data['data']['downloadPage']
        return None
    except Exception as e:
        return None

def upload_to_fileio(file_path):
    try:
        with open(file_path, 'rb') as file:
            response = requests.post('https://file.io/', 
                                   files={'file': file})
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['link']
        return None
    except Exception as e:
        return None

def upload_to_0x0(file_path):
    try:
        with open(file_path, 'rb') as file:
            response = requests.post('https://0x0.st', 
                                   files={'file': file})
        
        if response.status_code == 200:
            return response.text.strip()
        return None
    except Exception as e:
        return None

def download_file(user_id, filename):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        file_path = os.path.join(current_path, filename)
        
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            return f"❌ File '{filename}' not found or is a folder"
        
        file_size = get_file_size(file_path)
        results = []
        
        results.append(f"📤 Uploading '{filename}' ({file_size})...")
        
        gofile_link = upload_to_gofile(file_path)
        if gofile_link:
            results.append(f"🔗 GoFile: {gofile_link}")
        
        fileio_link = upload_to_fileio(file_path)
        if fileio_link:
            results.append(f"🔗 File.io: {fileio_link}")
        
        x0_link = upload_to_0x0(file_path)
        if x0_link:
            results.append(f"🔗 0x0.st: {x0_link}")
        
        if not any([gofile_link, fileio_link, x0_link]):
            results.append("❌ All upload services failed")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"❌ Download error: {e}"

def search_files(user_id, search_term):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        matches = []
        
        for item in os.listdir(current_path):
            if search_term.lower() in item.lower():
                item_path = os.path.join(current_path, item)
                if os.path.isdir(item_path):
                    matches.append(f"📁 {item}/")
                else:
                    size = get_file_size(item_path)
                    matches.append(f"📄 {item} ({size})")
        
        if matches:
            return f"🔍 Found {len(matches)} matches:\n" + "\n".join(matches[:20])
        else:
            return f"🔍 No files found matching '{search_term}'"
            
    except Exception as e:
        return f"❌ Search error: {e}"

def get_current_path(user_id):
    return current_paths.get(user_id, "C:\\")

def set_path(user_id, path):
    try:
        if os.path.exists(path) and os.path.isdir(path):
            current_paths[user_id] = path
            user_pages[user_id] = 1
            return get_file_tree(path, 1)
        else:
            return f"❌ Path '{path}' not found"
    except Exception as e:
        return f"❌ Path error: {e}"

def get_current_page(user_id):
    return user_pages.get(user_id, 1)

def upload_attachment(user_id, attachment_url, filename):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        file_path = os.path.join(current_path, filename)
        
        if os.path.exists(file_path):
            return f"❌ File '{filename}' already exists"
        
        response = requests.get(attachment_url, stream=True)
        response.raise_for_status()
        
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        file_size = get_file_size(file_path)
        return f"✅ Uploaded '{filename}' ({file_size}) to {current_path}"
        
    except requests.RequestException as e:
        return f"❌ Download failed: {e}"
    except PermissionError:
        return f"❌ Access denied - cannot write to {current_path}"
    except Exception as e:
        return f"❌ Upload error: {e}"

def create_folder(user_id, folder_name):
    try:
        current_path = current_paths.get(user_id, "C:\\")
        folder_path = os.path.join(current_path, folder_name)
        
        if os.path.exists(folder_path):
            return f"❌ Folder '{folder_name}' already exists"
        
        os.makedirs(folder_path)
        return f"✅ Created folder '{folder_name}' in {current_path}"
        
    except PermissionError:
        return f"❌ Access denied - cannot create folder in {current_path}"
    except Exception as e:
        return f"❌ Folder creation error: {e}"