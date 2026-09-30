"""A fixed illustration with local hand animation and eight registered gaze poses.

The raster artwork is unchanged. SVG clips share one source and one coordinate
system, so changing a pose cannot move the body, ears or laptop.
"""
DIRECTIONS = {
    'e': (7, 0), 'se': (5, 5), 's': (0, 6), 'sw': (-5, 5),
    'w': (-7, 0), 'nw': (-5, -5), 'n': (0, -6), 'ne': (5, -5),
}


def render():
    # Pixel-step outlines of the original dark eyes, in the first sprite cell.
    left = 'M223 267H240V277H247V307H242V314H238V318H235V322H217V317H212V312H208V288H213V278H216V272H223Z'
    right = 'M328 282H357V289H364V295H366V297H371V323H366V332H362V338H354V344H324V340H317V337H312V306H316V294H321V288H328Z'
    poses = ''.join(
        f'<g class="gaze-frame gaze-{name}"><use href="#pika-pupils" transform="translate({x} {y})"/></g>'
        for name, (x, y) in DIRECTIONS.items()
    )
    return f'''<div class="working-pika pika-motion" data-gaze="center" aria-hidden="true"><div class="motion-canvas">
<img class="motion-still" src="/assets/pika-working.png" alt="" width="1239" height="1269" fetchpriority="high">
<svg class="motion-art" viewBox="0 0 620 635" xmlns="http://www.w3.org/2000/svg" focusable="false">
<defs>
<image id="pika-sheet" href="/assets/pika-motion.png" width="1240" height="1269"/>
<clipPath id="pika-body"><rect width="616" height="635"/></clipPath>
<clipPath id="pika-eyes"><path d="{left}"/><path d="{right}"/></clipPath>
<g id="pika-pupils" clip-path="url(#pika-eyes)"><use href="#pika-sheet"/></g>
<clipPath id="pika-hand"><path d="M249 406H305V444H318V514H253V480H249Z"/></clipPath>
</defs>
<g clip-path="url(#pika-body)"><use class="motion-body" href="#pika-sheet"/></g>
<g class="motion-hand" clip-path="url(#pika-hand)"><use href="#pika-sheet" x="-608"/></g>
<g class="gaze-layer"><path d="{left}" fill="#f7d5a9"/><path d="{right}" fill="#f9d9ad"/>{poses}</g>
</svg></div></div>'''
