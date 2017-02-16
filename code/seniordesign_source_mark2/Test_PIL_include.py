import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from PIL import Image, ImageDraw

#--SET WINDOW SIZE
from kivy.config import Config
Config.set('graphics', 'width', '428')
Config.set('graphics', 'height', '240')
#--


HUD_WIDTH = 428 #428
HUD_HEIGHT = 240 #240
HUD_CENTER_X = HUD_WIDTH / 2 
HUD_CENTER_Y = HUD_HEIGHT / 2
SCOPE_WIDTH = HUD_HEIGHT
SCOPE_HEIGHT = SCOPE_WIDTH
GRAPH_OFFSET_LEFT_RIGHT = 10
GRAPH_OFFSET_TOP_BOTTOM = 40
GRAPH_WIDTH = 20
GRAPH_MAX_HEIGHT = HUD_HEIGHT - GRAPH_OFFSET_TOP_BOTTOM*2
RING_INITIAL_OFFSET = HUD_CENTER_X - (SCOPE_WIDTH/2)
RING_SUBSEQUENT_OFFSET = (SCOPE_WIDTH / 2) / 3
BLACK = (0, 0, 0)
LIME_GREEN = (10, 240, 25)

first_cycle = True

class HudApp(App):
	def build(self):
		global first_cycle
		layout = FloatLayout(size=(HUD_WIDTH, HUD_HEIGHT))
		
		if first_cycle:
			#Image 1
			display_image = Image.new("RGB", (HUD_WIDTH, HUD_HEIGHT), BLACK)
			draw = ImageDraw.Draw(display_image)
			draw.rectangle([(GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM),
									(GRAPH_OFFSET_LEFT_RIGHT + GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
									 fill=None, outline=LIME_GREEN)
							  
			#Scope (center)
			draw.ellipse([RING_INITIAL_OFFSET, 0, RING_INITIAL_OFFSET + SCOPE_WIDTH, HUD_HEIGHT],
						  outline=LIME_GREEN)
			draw.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET, RING_SUBSEQUENT_OFFSET, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET],
						  outline=LIME_GREEN)
			draw.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET*2, RING_SUBSEQUENT_OFFSET*2, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET*2, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET*2],
						  outline=LIME_GREEN)
			draw.ellipse([RING_INITIAL_OFFSET + RING_SUBSEQUENT_OFFSET*3, RING_SUBSEQUENT_OFFSET*3, RING_INITIAL_OFFSET + SCOPE_WIDTH - RING_SUBSEQUENT_OFFSET*3, HUD_HEIGHT - RING_SUBSEQUENT_OFFSET*3],
						  outline=LIME_GREEN)

			#Paint (right)
			draw.rectangle([(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT - GRAPH_WIDTH, GRAPH_OFFSET_TOP_BOTTOM),
							(HUD_WIDTH - GRAPH_OFFSET_LEFT_RIGHT, GRAPH_OFFSET_TOP_BOTTOM + GRAPH_MAX_HEIGHT)],
							 fill=None, outline=LIME_GREEN)
			filename = "HUD_display.png"
			display_image.save(filename)

			#Image 2
			display_image2 = Image.new("RGBA", (HUD_WIDTH, HUD_HEIGHT)) # !!!RGBA allows for transparancy!!!
			draw = ImageDraw.Draw(display_image2)
			draw.ellipse((25, 25, 75, 75), fill=(255, 0, 0))
			filename =  "second_layer.png"
			display_image2.save(filename)

			#Paste Image 3 on top
			base_layer = Image.open('HUD_display.png')
			top_layer = Image.open('second_layer.png')
			base_layer.paste(top_layer, top_layer)
			filename = "HUD_display_trans.png"
			base_layer.save(filename)
			
			first_cycle = False
			
		else:
			pass
		
		try:
			img = AsyncImage(source='HUD_display_trans.png')
			layout.add_widget(img)
		except:
			print 'No image found...'

		
			
		return layout

HudApp().run()