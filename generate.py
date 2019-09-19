import jinja2, yaml, os, re#,cairosvg
import subprocess, textwrap

kartoj = yaml.safe_load(open("kartoj.yaml").read())   # listo de kartoj

BILDETO = """<circle x="-800" y="-230300" r="10" stroke="#62bfd2" stroke-width="1.5" fill="#4f92b2" />
             <image  x="-800" y="-230300" height="14" width="14" xlink:href="{}.svg" />"""

for k in kartoj: #trancxu tekston al sammlongaj lineoj
    splitText = textwrap.wrap(k["teksto"], 27)
    k["svg"] = k["bildo"] if os.path.isfile(k["bildo"]) else "akvobotelo.svg"
    if "{{" in k["teksto"]:
        repalceStr = k["teksto"].split("{{")[1].split("}}")[0]
        splitText = [(t.split("}}")[1] if "}}" in t else t).strip() for k in splitText for t in k.split("{{") ]
        print(splitText, "\n\n")
    k["teksto"] = splitText

kartoj = [k for k in kartoj for i in range(k["kvanto"])] # adpatas la liston por kvanto de karto
pagxoj = [kartoj[i:i+9] for i in range(0, len(kartoj), 9)] #disigas la kartaro en pagxojn po de 9 kartoj

for i, pagxo in enumerate(pagxoj):
    template_str = open("templates/sxablono.svg.jinja2").read()
    t = jinja2.Template(template_str)
    kartoj_offsets = zip(pagxo, [(0,0), (61,0), (122,0), (0,91), (61,91), (122,91), (0,182), (61,182), (122,182)])
    r = t.render(kartoj_offsets=kartoj_offsets)
    open('svg/{}.svg'.format(i), "w").write(r)
    subprocess.check_output(['inkscape','-z', '--export-dpi', '300', 'svg/{}.svg'.format(i), '-e', 'img/{}.png'.format(i)])
subprocess.check_output(['convert', 'img/[0-9]*.png', 'ludo.pdf'])
