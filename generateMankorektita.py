for i in range(12):
    subprocess.check_output(['inkscape','-z', '--export-dpi', '300', 'svg/{}.svg'.format(i), '-e', 'img/{}.png'.format(i)])
subprocess.check_output(['convert', 'img/[0-9]*.png', 'ludo.pdf'])
