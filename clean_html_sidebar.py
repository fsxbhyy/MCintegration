from bs4 import BeautifulSoup

def remove_class_prefix_from_sidebar(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # 找 class="sphinxsidebarwrapper" 侧边栏
    sidebar = soup.find('div', class_='sphinxsidebarwrapper')
    
    if sidebar:
        # 找 class="pre" 的 span 标签
        for span in sidebar.find_all('span', class_='pre'):
            text = span.get_text()
            # 删除 '.' 之前的内容
            if '.' in text:
                method_name = text.split('.')[1] 
                # 更新 <a> 标签，保证跳转有效
                for a_tag in sidebar.find_all('a', class_='reference internal'):
                    if text in a_tag.get_text():
                        href = a_tag['href']
                        new_href = href.replace(text, method_name)
                        a_tag['href'] = new_href
                        print(f"Updated href: {href} -> {new_href}")
                new_span = soup.new_tag("span", **{"class": "pre"})
                new_span.string = method_name
                span.replace_with(new_span)

        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Successfully wrote changes back to {html_file}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        print("No sidebar found in the HTML.")

input_html = './build/html/src.html'
remove_class_prefix_from_sidebar(input_html)