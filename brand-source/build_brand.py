from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
import json
root=Path(__file__).resolve().parents[1];out=root/'public/brand'
font=TTFont(root/'brand-source/Manrope.ttf');(root/'public/fonts/manrope-variable.ttf').write_bytes((root/'brand-source/Manrope.ttf').read_bytes())
fonts={w:instantiateVariableFont(font,{'wght':w},inplace=False) for w in [500,600,700,800]}
colors={'navy':'#102A56','blue':'#2165DB','green':'#16A075','gold':'#F2C64D','coral':'#EF8956','ink':'#162D50','muted':'#596A82','paper':'#F4F7FC'}
def text(t,x,y,size,fill,w=700,spacing=0):
 f=fonts[w];gs=f.getGlyphSet();cmap=f.getBestCmap();units=f['head'].unitsPerEm;s=size/units;cursor=0;shapes=[]
 for c in t:
  name=cmap.get(ord(c),'space');pen=SVGPathPen(gs);gs[name].draw(pen);shapes.append(f'<path d="{pen.getCommands()}" transform="translate({cursor:.3f} 0)"/>');cursor+=gs[name].width+spacing/s
 return f'<g fill="{fill}" transform="translate({x} {y}) scale({s} {-s})">'+''.join(shapes)+'</g>'
def symbol(x=0,y=0,scale=1,mono=None):
 return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"><path stroke="{mono or colors["blue"]}" d="M53 102 C23 95 18 67 29 44 C42 17 77 16 93 42 C101 55 101 66 95 79"/><path stroke="{mono or colors["green"]}" d="M92 44 C112 22 146 30 154 56 C164 86 143 108 119 110 C105 111 95 106 88 95"/><path stroke="{mono or colors["gold"]}" d="M123 109 C126 140 95 156 71 145 C44 133 39 104 53 84 C61 74 72 70 85 72"/></g>'
def svg(w,h,content):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{content}</svg>'
def logo(light=False,mono=False):
 ink='#FFFFFF' if light else colors['navy'];sym=symbol(4,7,.58,ink if mono else None)
 return sym+text('ELO',118,66,67,ink,800,-1)+text('NOVO MUNDO',121,96,16,ink,700,2)
for name,light,mono in [('elo-horizontal',False,False),('elo-horizontal-claro',True,False),('elo-monocromatico',False,True)]:
 (out/f'{name}.svg').write_text(svg(300,114,logo(light,mono)))
(out/'elo-assinatura.svg').write_text(svg(560,170,f'<g transform="translate(80 0)">{logo()}</g>'+text('Educação, Ligação e Organização',40,151,24,colors['muted'],500)))
(out/'elo-simbolo.svg').write_text(svg(176,168,symbol()))
for name,bg in [('elo-app-icon',colors['navy']),('elo-app-icon-maskable',colors['navy'])]:
 scale=1.7 if 'maskable' in name else 2.12
 x=(512-176*scale)/2;y=(512-168*scale)/2
 (out/f'{name}.svg').write_text(svg(512,512,f'<rect width="512" height="512" rx="{0 if "maskable" in name else 112}" fill="{bg}"/>'+symbol(x,y,scale)))
(out/'elo-padrao.svg').write_text(svg(800,800,'<defs><pattern id="p" width="210" height="210" patternUnits="userSpaceOnUse">'+symbol(32,25,.7,'#2165DB')+'</pattern></defs><rect width="800" height="800" fill="#F4F7FC"/><rect width="800" height="800" fill="url(#p)" opacity=".065"/>'))
# Editorial banner and launch screen: exact vector text and vector artwork.
(out/'elo-banner.svg').write_text(svg(1600,500,'<rect width="1600" height="500" fill="#102A56"/>'+symbol(1090,57,2.25)+f'<g transform="translate(85 64)">{logo(True)}</g>'+text('Educação, Ligação',90,300,60,'#FFFFFF',700,-1)+text('e Organização.',90,379,60,'#FFFFFF',700,-1)+text('Um novo mundo de conexões.',92,447,24,'#BDD1F3',500)))
(out/'elo-splash.svg').write_text(svg(1080,1920,'<rect width="1080" height="1920" fill="#102A56"/>'+symbol(320,480,2.5)+text('ELO',287,1130,250,'#FFFFFF',800,-7)+text('NOVO MUNDO',291,1235,59,'#FFFFFF',700,5)+text('Educação, Ligação',270,1500,52,'#CDDAED',500)+text('e Organização.',334,1575,52,'#CDDAED',500)))
(out/'design-tokens.json').write_text(json.dumps({'brand':'ELO Novo Mundo','meaning':'Educação, Ligação e Organização','colors':colors,'font':'Manrope','radius':{'small':8,'card':14,'hero':20},'space':[4,8,12,16,24,32,48,64]},ensure_ascii=False,indent=2))
# Contact sheet for visual QA; all wordmarks outlined, independent of installed fonts.
board='<rect width="1600" height="1050" fill="#F4F7FC"/>'+text('ELO NOVO MUNDO',65,70,22,colors['navy'],800,1)+text('Identidade digital • 2026',1200,70,18,colors['muted'],500)
board+='<rect x="50" y="110" width="960" height="465" rx="20" fill="white"/>'+f'<g transform="translate(260 185) scale(1.7)">{logo()}</g>'+text('Educação, Ligação e Organização',220,470,30,colors['muted'],500)
board+='<rect x="1035" y="110" width="515" height="465" rx="20" fill="#102A56"/>'+symbol(1150,175,1.65)+text('ELO',1190,495,80,'white',800)
for i,(n,k) in enumerate([('Azul mundo','navy'),('Conexão','blue'),('Crescimento','green'),('Descoberta','gold'),('Acolhimento','coral')]):
 x=50+i*305;board+=f'<rect x="{x}" y="605" width="285" height="135" rx="14" fill="{colors[k]}"/>'+text(n,x+3,776,18,colors['navy'],700)+text(colors[k],x+3,808,16,colors['muted'],500)
board+=text('Uma marca para aproximar pessoas e organizar o ensino.',65,916,32,colors['navy'],600)+text('Logo vetorial • ícones de aplicativo • capa • tela de abertura • arte de boas-vindas',65,976,19,colors['muted'],500)
(root/'brand-source/brand-board.svg').write_text(svg(1600,1050,board))
