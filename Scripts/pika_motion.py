"""Registered gaze poses with a small, anchored upper-body lean.

The raster artwork is unchanged. A displacement weight fades toward the feet
and is zero across the laptop; no independently drawn full-body frames switch.
"""
DIRECTIONS = {
    'e': (7, 0), 'ese': (6, 2), 'se': (5, 4), 'sse': (3, 6),
    's': (0, 6), 'ssw': (-3, 6), 'sw': (-5, 4), 'wsw': (-6, 2),
    'w': (-7, 0), 'wnw': (-6, -2), 'nw': (-5, -4), 'nnw': (-3, -6),
    'n': (0, -6), 'nne': (3, -6), 'ne': (5, -4), 'ene': (6, -2),
}


def render():
    # Pixel-step outlines of the original dark eyes, in the first sprite cell.
    left = 'M223 267H240V277H247V307H242V314H238V318H235V322H217V317H212V312H208V288H213V278H216V272H223Z'
    right = 'M328 282H357V289H364V295H366V297H371V323H366V332H362V338H354V344H324V340H317V337H312V306H316V294H321V288H328Z'
    poses = ''.join(
        f'<g class="gaze-frame gaze-{name}" style="--look-x:{x}px;--look-y:{y}px"><use href="#pika-pupils"/></g>'
        for name, (x, y) in DIRECTIONS.items()
    )
    filters = ''.join(
        f'<filter id="pika-{kind}-{name}" x="-20" y="-20" width="660" height="675" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse" color-interpolation-filters="sRGB">'
        '<feImage href="/assets/pika-lean-map.svg" x="-20" y="-20" width="660" height="675" result="weight"/>'
        '<feComponentTransfer in="weight" result="offset">'
        f'<feFuncR type="linear" slope="{-x / 14:g}" intercept="0.5"/>'
        f'<feFuncG type="linear" slope="{-y / 24:g}" intercept="0.5"/>'
        '</feComponentTransfer>'
        f'<feDisplacementMap in="SourceGraphic" in2="offset" scale="{scale}" xChannelSelector="R" yChannelSelector="G"/>'
        '</filter>'
        for name, (x, y) in DIRECTIONS.items()
        for kind, scale in [('lean', 24), ('soft', 12)]
    )
    return f'''<div class="working-pika pika-motion" data-gaze="center" aria-hidden="true"><div class="motion-canvas">
<img class="motion-still" src="/assets/pika-working.png" alt="" width="1239" height="1269" fetchpriority="high">
<svg class="motion-art" viewBox="0 0 620 635" xmlns="http://www.w3.org/2000/svg" focusable="false">
<defs>
{filters}
<image id="pika-sheet" href="/assets/pika-motion.png" width="1240" height="1269"/>
<clipPath id="pika-body"><rect width="616" height="635"/></clipPath>
<clipPath id="pika-eyes"><path d="{left}"/><path d="{right}"/></clipPath>
<g id="pika-pupils" clip-path="url(#pika-eyes)"><use href="#pika-sheet"/></g>
<clipPath id="pika-hand"><path d="M249 406H305V444H318V514H253V480H249Z"/></clipPath>
</defs>
<g class="motion-figure">
<g clip-path="url(#pika-body)"><use class="motion-body" href="#pika-sheet"/></g>
<g class="motion-hand" clip-path="url(#pika-hand)"><use href="#pika-sheet" x="-608"/></g>
<g class="gaze-layer"><path d="{left}" fill="#f7d5a9"/><path d="{right}" fill="#f9d9ad"/>{poses}</g>
</g></svg></div></div>'''
