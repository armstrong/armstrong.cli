from lxml import etree


def import_wordpress(import_file=None, dryrun=False):
    parser = etree.XMLParser(recover=True)
    xml = etree.parse(import_file, parser)
    root = xml.getroot()
    channel = find(root, 'channel')
    for tag in channel.findall('wp:tag', namespaces=root.nsmap):
        handle_tag(tag)
    for category in channel.findall('wp:category', namespaces=root.nsmap):
        handle_category(category)
    for item in channel.findall('item'):
        handle_item(item)

def find(item, tag):
    return item.find(tag, namespaces=item.nsmap)

def handle_item(item):
    title = find(item, 'title').text
    post_type = find(item, 'wp:post_type').text
    title = find(item, 'title').text
    content = find(item, 'content:encoded').text
    author = find(item, 'dc:creator').text
    date = find(item, 'wp:post_date').text
    print 'Title: %s - %s' % (title, post_type)
    print 'Author: %s - %s' % (author, date)
    print 'Content: %s' % content

def handle_tag(tag):
    print 'Tag: %s, %s' % (find(tag, 'wp:tag_slug').text,
            find(tag, 'wp:tag_name').text)

def handle_category(cat):
    print 'Category: %s, %s' % (\
            find(cat, 'wp:category_nicename').text,
            find(cat, 'wp:cat_name').text)
