import os
from markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    page_content = page_content.replace('href="/', f'href="{basepath}')
    page_content = page_content.replace("src=\"/", f'src=\"{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                rel_dir = os.path.relpath(root, dir_path_content)
                rel_dir = '' if rel_dir == '.' else rel_dir
                dest_dir = os.path.join(dest_dir_path, rel_dir)
                dest_file = os.path.splitext(file)[0] + '.html'
                dest_path = os.path.join(dest_dir, dest_file)
                from_path = os.path.join(root, file)
                generate_page(from_path, template_path, dest_path, basepath)
