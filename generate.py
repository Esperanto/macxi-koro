import jinja2, yaml, os, cairosvg
import subprocess, textwrap

kartoj = yaml.safe_load(open("kartoj.yaml").read())   # listo de kartoj

for k in kartoj: #trancxu tekston al sammlongaj lineoj
    k["teksto"] = textwrap.wrap(k["teksto"], 27)
    k["svg"] = k["bildo"] if os.path.isfile(k["bildo"]) else "akvobotelo.svg"
kartoj = [k for k in kartoj for i in range(k["kvanto"])] # adpatas la liston por kvanto de karto
pagxoj = [kartoj[i:i+9] for i in range(0, len(kartoj), 9)] #disigas la kartaro en pagxojn po de 9 kartoj

for i, pagxo in enumerate(pagxoj):
    template_str = open("templates/sxablono.svg.jinja2").read()
    t = jinja2.Template(template_str)
    kartoj_offsets = zip(pagxo, [(0,0), (61,0), (122,0), (0,91), (61,91), (122,91), (0,182), (61,182), (122,182)])
    r = t.render(kartoj_offsets=kartoj_offsets)
    open('svg/{}.svg'.format(i), "w").write(r)
    cairosvg.svg2png(
        url='svg/{}.svg'.format(str(i)),
        write_to='img/{}.png'.format(str(i)),
        dpi=300
    )
subprocess.check_output(['convert', 'img/[0-9]*.png', 'ludo.pdf'])
