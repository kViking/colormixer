def set_current_state(page, bgcolor, complementary, palette=None, palette_colors=None):
    page.session.set('current', {
        'bgcolor': bgcolor,
        'complementary': complementary,
        'palette': palette,
        'palette_colors': palette_colors or []
    })

def get_current_state(page):
    val = page.session.get('current')
    return val if val is not None else {}
