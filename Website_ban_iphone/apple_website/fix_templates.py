import pathlib
p = pathlib.Path('home/templates')
pattern = "{% url 'product_detail' %}"
replacement = "{% if product %}{% url 'product_detail_slug' slug=product.slug %}{% else %}{% url 'iphone' %}{% endif %}"
for f in p.rglob('*.html'):
    text = f.read_text(encoding='utf-8')
    if pattern in text:
        new = text.replace(pattern, replacement)
        f.write_text(new, encoding='utf-8')
        print('Updated', f)
print('Done')
