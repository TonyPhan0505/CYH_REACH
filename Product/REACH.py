import pygame
from pygame import mixer
import random
import getpass
import time
import os
from playsound import playsound
import sqlite3

def main():

	pygame.init()
	mixer.init()

	screen = pygame.display.set_mode((1277,690))
	pygame.display.set_caption("REACH")

	path = str(os.path.dirname(os.path.realpath(__file__))) + "/"
	
	mixer.music.load(path+"MEDIA/intro.mp3")
	mixer.music.set_volume(0.7)
	mixer.music.play()

	master = Game_Master(screen, path)
	master.play()

	pygame.quit()

class Game_Master:
	def __init__(self, screen, path):

		########## Game's master tools #######
		self.screen = screen
		self.path = path
		self.close_clicked = False
		self.game_clock = pygame.time.Clock()
		self.FPS = 40
		self.music_on = True
		self.game_start_time = time.time()
		self.time_of_inactivity = 0

		self.reception_on = True
		self.waiting_room_on = False
		self.exhibition_room_on = False
		self.room1_on = False
		self.room2_on = False
		self.tutorial_room_on = False

		self.solved = 0
		self.quickest_case = "..."
		self.total_time = 0
		self.skills_mastered = 0
		######################################

		##################### Room 1's master tools #####################
		# Check for open bags and items in room 1
		self.room1_bag1_opened = False
		self.room1_bag2_opened = False
		self.room1_bag3_opened = False
		self.room1_bag4_opened = False
		self.room1_bag5_opened = False
		self.room1_bag6_opened = False
		self.room1_bag7_opened = False
		self.room1_bag8_opened = False
		self.room1_bag9_opened = False
		self.room1_bag10_opened = False
		self.room1_targets_doctors_note_opened = False
		self.room1s_signs_opened = False

		# answering tools in room 1
		self.room1_john_paul_picked = False
		self.room1_wrong_answer_picked = False
		self.room1s_solution_button_on = False
		self.room1s_solution_on = False

		# Time trackers in game rooms
		self.room_start_time = 0
		self.room_time_left = 600

		# Room 1's teacher's position and velocity trackers
		self.teacher_pos = [600, 220]
		self.teacher_velocity = [3,0]
		#################################################################

		##################### Room 2's master tools #####################
		self.room2s_journal_opened = False
		self.room2s_phone_opened = False
		self.room2s_water_bottle_opened = False
		self.room2s_suitcase_opened = False
		self.room2s_note_opened = False
		self.room2s_box_opened = False
		self.room2s_answer_button_pressed = False
		self.room2s_spaces_filled = 0
		self.letters_pressed = []
		self.room2s_solution_on = False
		self.room2s_signs_opened = False
		#################################################################
	
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.close_clicked = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.reception_on:
						if (self.screen.get_width()-155-155 <= event.pos[0] <= self.screen.get_width()-155) and (370 <= event.pos[1] <= (370+40)):
							self.reception_on = False
							self.solved = self.get_stats()[0]
							self.quickest_case = self.get_stats()[1]
							self.total_time = self.get_stats()[2]
							self.skills_mastered = self.get_stats()[3]
							self.waiting_room_on = True
						elif (self.screen.get_width()-155-155 <= event.pos[0] <= self.screen.get_width()-155) and (470 <= event.pos[1] <= (470+40)):
							self.reception_on = False
							self.exhibition_room_on = True
						elif (self.screen.get_width()-155-155 <= event.pos[0] <= self.screen.get_width()-155) and (570 <= event.pos[1] <= (570+40)):
							if self.music_on:
								self.music_on = False
								mixer.music.stop()
							else:
								self.music_on = True
								mixer.music.play()
							
					elif self.waiting_room_on:
						self.room_start_time = 0
						self.room_time_left = 600
						if (self.screen.get_width()-130-155 <= event.pos[0] <= self.screen.get_width()-130) and (110 <= event.pos[1] <= (110+40)):
							self.waiting_room_on = False
							self.room1_on = True
							self.room_start_time = time.time()
							mixer.music.stop()
							mixer.music.load(self.path+"MEDIA/bird.mp3")
							mixer.music.set_volume(0.7)
							mixer.music.play()
						elif (self.screen.get_width()-130-155 <= event.pos[0] <= self.screen.get_width()-130) and (200 <= event.pos[1] <= (200+40)):
							self.waiting_room_on = False
							self.room2_on = True
							self.room_start_time = time.time()
							mixer.music.stop()
							mixer.music.load(self.path+"MEDIA/train.mp3")
							mixer.music.set_volume(0.7)
							mixer.music.play()
						elif (self.screen.get_width()-130-155 <= event.pos[0] <= self.screen.get_width()-130) and (470 <= event.pos[1] <= (470+40)):
							self.waiting_room_on = False
							self.tutorial_room_on = True
						elif (self.screen.get_width()-130-155 <= event.pos[0] <= self.screen.get_width()-130) and (560 <= pygame.mouse.get_pos()[1] <= (560+40)):
							if self.music_on:
								self.music_on = False
								mixer.music.stop()
							else:
								self.music_on = True
								mixer.music.play()
					
					elif self.exhibition_room_on:
						if (800 <= event.pos[0] <= 800+90) and (590 <= event.pos[1] <= (590+40)):
							self.reception_on = True
							self.exhibition_room_on = False

					elif self.room1_on:
						if (0 <= event.pos[0] <= 90) and (self.screen.get_height()-40 <= event.pos[1] <= self.screen.get_height()):
							if self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
								self.add_records(1, 5, 600-self.room_time_left, 1)
							self.solved = self.get_stats()[0]
							self.quickest_case = self.get_stats()[1]
							self.total_time = self.get_stats()[2]
							self.skills_mastered = self.get_stats()[3]
							self.waiting_room_on = True
							self.room1_on = False
							self.room1_john_paul_picked = False
							self.room1_wrong_answer_picked = False
							self.room1s_solution_button_on = False
							self.room1s_solution_on = False
							self.teacher_pos = [600, 220]
							self.teacher_velocity = [3,0]
							self.room1_bag1_opened = False
							self.room1_bag2_opened = False
							self.room1_bag3_opened = False
							self.room1_bag4_opened = False
							self.room1_bag5_opened = False
							self.room1_bag6_opened = False
							self.room1_bag7_opened = False
							self.room1_bag8_opened = False
							self.room1_bag9_opened = False
							self.room1_bag10_opened = False
							self.room1_targets_doctors_note_opened = False
							self.room1s_signs_opened = False
							mixer.music.stop()
							mixer.music.load(self.path+"MEDIA/intro.mp3")
							mixer.music.set_volume(0.7)
							mixer.music.play()
						elif (295+50 <= event.pos[0] <= 295+50+40) and (340 <= event.pos[1] <= 340+40):
							self.room1_bag1_opened = True
						elif self.room1_bag1_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag1_opened = False
						elif (295+160+50 <= event.pos[0] <= 295+160+50+40) and (340 <= event.pos[1] <= 340+40):
							self.room1_bag2_opened = True
						elif self.room1_bag2_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag2_opened = False
						elif (295+160*2+50 <= event.pos[0] <= 295+160*2+50+40) and (340 <= event.pos[1] <= 340+40):
							self.room1_bag3_opened = True
						elif self.room1_bag3_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag3_opened = False
						elif (295+160*3+50 <= event.pos[0] <= 295+160*3+50+40) and (340 <= event.pos[1] <= 340+40):
							self.room1_bag4_opened = True
						elif self.room1_bag4_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag4_opened = False
						elif (295+160*4+50 <= event.pos[0] <= 295+160*4+50+40) and (340 <= event.pos[1] <= 340+40):
							self.room1_bag5_opened = True
						elif self.room1_bag5_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag5_opened = False
						elif (295+50 <= event.pos[0] <= 295+50+40) and (490 <= event.pos[1] <= 490+40):
							self.room1_bag6_opened = True
						elif self.room1_bag6_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag6_opened = False
						elif (295+160+50 <= event.pos[0] <= 295+160+50+40) and (490 <= event.pos[1] <= 490+40):
							self.room1_bag7_opened = True
						elif self.room1_bag7_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag7_opened = False
						elif (295+160*2+50 <= event.pos[0] <= 295+160*2+50+40) and (490 <= event.pos[1] <= 490+40):
							self.room1_bag8_opened = True
						elif self.room1_bag8_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag8_opened = False
						elif (295+160*3+50 <= event.pos[0] <= 295+160*3+50+40) and (490 <= event.pos[1] <= 490+40):
							self.room1_bag9_opened = True
						elif self.room1_bag9_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag9_opened = False
						elif (295+160*4+50 <= event.pos[0] <= 295+160*4+50+40) and (490 <= event.pos[1] <= 490+40):
							self.room1_bag10_opened = True
						elif self.room1_bag10_opened and ((self.screen.get_width()//2)+300+30 <= event.pos[0] <= (self.screen.get_width()//2)+300+30+50) and ((self.screen.get_height()//2)-(330//2) <= event.pos[1] <= (self.screen.get_height()//2)-(330//2)+50):
							self.room1_bag10_opened = False
						elif (self.screen.get_width()-40 <= event.pos[0] <= self.screen.get_width()) and (self.screen.get_height()-40 <= event.pos[1] <= self.screen.get_height()):
							self.room1_targets_doctors_note_opened = True
						elif self.room1_targets_doctors_note_opened and ((self.screen.get_width()//2)+100+30 <= event.pos[0] <= (self.screen.get_width()//2)+100+30+50) and ((self.screen.get_height()//2)-100 <= event.pos[1] <= (self.screen.get_height()//2)-100+50):
							self.room1_targets_doctors_note_opened = False
						elif (532 <= event.pos[0] <= 532 + 71) and (99 <= event.pos[1] <= 99+83):
							self.room1_john_paul_picked = True
						elif ((461 <= event.pos[0] <= 461 + 71) or (532+71 <= event.pos[0] <= 532+71*3)) and (12 <= event.pos[1] <= 12+83*2):
							self.room1_wrong_answer_picked = True
						elif ((self.screen.get_width()//2 - 60) <= event.pos[0] <= (self.screen.get_width()//2 - 60) + 120) and (430 <= event.pos[1] <= 430+40) and self.room1s_solution_button_on:
							self.room1s_solution_on = True
						elif self.room1s_solution_on and ((self.screen.get_width()//2)+(650//2)+30 <= event.pos[0] <= (self.screen.get_width()//2)+(650//2)+30+50) and ((self.screen.get_height()//2)-(400//2) <= event.pos[1] <= (self.screen.get_height()//2)-(400//2)+50):
							self.room1s_solution_on = False
						elif self.room1s_solution_on and (798 <= event.pos[0] <= 942) and (165 <= event.pos[1] <= 207):
							self.room1s_solution_on = False
							self.room1s_signs_opened = True
						elif self.room1s_signs_opened and (922 <= event.pos[0] <= 950) and (157 <= event.pos[1] <= 186):
							self.room1s_signs_opened = False
					
					elif self.room2_on:
						if (self.screen.get_width()-90 <= event.pos[0] <= self.screen.get_width()) and (self.screen.get_height()-40 <= event.pos[1] <= self.screen.get_height()):
							if self.letters_pressed == ["J","A","Y","D","E","N","S","M","I","T","H"]:
								self.add_records(2, 5, 600-self.room_time_left, 1)
							self.solved = self.get_stats()[0]
							self.quickest_case = self.get_stats()[1]
							self.total_time = self.get_stats()[2]
							self.skills_mastered = self.get_stats()[3]
							self.letters_pressed = []
							self.room2s_spaces_filled = 0
							self.waiting_room_on = True
							self.room2_on = False
							self.room2s_journal_opened = False
							self.room2s_phone_opened = False
							self.room2s_water_bottle_opened = False
							self.room2s_suitcase_opened = False
							self.room2s_note_opened = False
							self.room2s_box_opened = False
							self.room2s_solution_on = False
							self.room2s_signs_opened = False
							mixer.music.stop()
							mixer.music.load(self.path+"MEDIA/intro.mp3")
							mixer.music.set_volume(0.7)
							mixer.music.play()
						
						if not self.room2s_answer_button_pressed:
							if len(self.letters_pressed) < 11:
								if (40 <= event.pos[0] <= 100) and (621 <= event.pos[1] <= 683):
									self.room2s_journal_opened = True
								elif self.room2s_journal_opened and (895 <= event.pos[0] <= 928) and (192 <= event.pos[1] <= 223):
									self.room2s_journal_opened = False
								elif (95 <= event.pos[0] <= 164) and (563 <= event.pos[1] <= 620):
									self.room2s_phone_opened = True
								elif self.room2s_phone_opened and (609 <= event.pos[0] <= 672) and (521 <= event.pos[1] <= 580):
									self.room2s_phone_opened = False
								elif (403 <= event.pos[0] <= 500) and (288 <= event.pos[1] <= 461):
									self.room2s_suitcase_opened = True
								elif self.room2s_suitcase_opened and (893 <= event.pos[0] <= 934) and (183 <= event.pos[1] <= 222):
									self.room2s_suitcase_opened = False
								elif (506 <= event.pos[0] <= 532) and (419 <= event.pos[1] <= 452):
									self.room2s_note_opened = True
								elif self.room2s_note_opened and (817 <= event.pos[0] <= 836) and (149 <= event.pos[1] <= 167):
									self.room2s_note_opened = False
								elif (173 <= event.pos[0] <= 205) and (492 <= event.pos[1] <= 597):
									self.room2s_water_bottle_opened = True
								elif self.room2s_water_bottle_opened and (611 <= event.pos[0] <= 670) and (511 <= event.pos[1] <= 566):
									self.room2s_water_bottle_opened = False
								elif (192 <= event.pos[0] <= 288) and (625 <= event.pos[1] <= self.screen.get_height()):
									self.room2s_box_opened = True
								elif self.room2s_box_opened and (624 <= event.pos[0] <= 656) and (106 <= event.pos[1] <= 137):
									self.room2s_box_opened = False
								elif (self.screen.get_width()-90-30-100 <= event.pos[0] <= self.screen.get_width()-90-30) and (self.screen.get_height()-40 <= event.pos[1] <= self.screen.get_height()):
									self.room2s_answer_button_pressed = True
							else:
								if (557 <= event.pos[0] <= 721) and (383 <= event.pos[1] <= 415):
									self.room2s_solution_on = True
								elif self.room2s_solution_on and (868 <= event.pos[0] <= 886) and (200 <= event.pos[1] <= 213):
									self.room2s_solution_on = False
								elif self.room2s_solution_on and (742 <= event.pos[0] <= 857) and (226 <= event.pos[1] <= 251):
									self.room2s_solution_on = False
									self.room2s_signs_opened = True
								elif self.room2s_signs_opened and (868 <= event.pos[0] <= 886) and (200 <= event.pos[1] <= 213):
									self.room2s_signs_opened = False
						else:
							if (927 <=event.pos[0] <= 952) and (188 <= event.pos[1] <= 214):
								self.room2s_answer_button_pressed = False
								self.room2s_spaces_filled = 0
								self.letters_pressed = []
							elif (314 <= event.pos[0] <= 964) and (297 <= event.pos[1] <= 398):
								self.room2s_spaces_filled += 1
								self.letters_pressed.append(self.find_letter_pressed(event.pos))
							elif (890 <= event.pos[0] <= 952) and (242 <= event.pos[1] <= 265) and self.room2s_spaces_filled > 0:
								self.room2s_spaces_filled -= 1
								self.letters_pressed.pop()

					elif self.tutorial_room_on:
						if (807 <= event.pos[0] <= 1126) and (498 <= event.pos[1] <= 568):
							self.tutorial_room_on = False
							self.waiting_room_on = True
							mixer.music.load(self.path+"MEDIA/intro.mp3")
							mixer.music.set_volume(0.7)
							mixer.music.play()

					playsound(self.path+"MEDIA/button_hovered.wav")
	def play(self):
		while not self.close_clicked:
			self.handle_events()
			self.draw()
			self.game_clock.tick(self.FPS)

	def draw(self):
		if self.reception_on:
			self.draw_reception()
		elif self.waiting_room_on:
			self.draw_waiting_room()
		elif self.exhibition_room_on:
			self.draw_exhibition_room()
		elif self.room1_on:
			self.draw_room1()
		elif self.room2_on:
			self.draw_room2()
		elif self.tutorial_room_on:
			self.draw_tutorial_room()
		pygame.display.flip()

	def draw_reception(self):
		intro_image = pygame.image.load(f"{self.path}MEDIA/intro.png")
		self.screen.blit(intro_image, (0,0))

		text_color = pygame.Color("white")
		text_font = pygame.font.SysFont("Calibri", 12, bold = True, italic = False)

		time_string = time.asctime()
		time_image = text_font.render(time_string, True, text_color)
		time_left_top = (self.screen.get_width() - time_image.get_width() - 10, 10)
		self.screen.blit(time_image, time_left_top)

		username_string = getpass.getuser()
		username_image = text_font.render(username_string, True, text_color)
		username_left_top = (time_left_top[0] - 30 - username_image.get_width(), 10)
		self.screen.blit(username_image, username_left_top)

		if (self.screen.get_width()-155-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-155) and (370 <= pygame.mouse.get_pos()[1] <= (370+40)):
			enter_game_button_color = pygame.Color("black")
			enter_game_button_width = 170
			enter_game_button_height = 50
		else:
			enter_game_button_color = pygame.Color("grey")
			enter_game_button_width = 155
			enter_game_button_height = 40
		enter_game_button = Button(self.screen, enter_game_button_color, self.screen.get_width()-155-enter_game_button_width, 370, enter_game_button_width, enter_game_button_height, "New Game")
		enter_game_button.draw()

		if (self.screen.get_width()-155-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-155) and (470 <= pygame.mouse.get_pos()[1] <= (470+40)):
			about_button_color = pygame.Color("black")
			about_button_width = 170
			about_button_height = 50
		else:
			about_button_color = pygame.Color("grey")
			about_button_width = 155
			about_button_height = 40
		about_button = Button(self.screen, about_button_color, self.screen.get_width()-155-about_button_width, 470, about_button_width, about_button_height, "About the Game")
		about_button.draw()

		if (self.screen.get_width()-155-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-155) and (570 <= pygame.mouse.get_pos()[1] <= (570+40)):
			music_off_button_color = pygame.Color("black")
		else:
			music_off_button_color = pygame.Color("grey")
		if self.music_on:
			music_control_button_text = "Music Off"
		else:
			music_control_button_text = "Music On"
		music_control_button = Button(self.screen, music_off_button_color, self.screen.get_width()-155-155, 570, 155, 40, music_control_button_text)
		music_control_button.draw()

		self.time_of_inactivity = int(time.time() - self.game_start_time)
		if self.time_of_inactivity >= 60*5:
			game_systems_time_out = pygame.image.load(self.path+"MEDIA/game_systems_time_out.png")
			self.screen.blit(game_systems_time_out, (0,0))

	def draw_waiting_room(self):
		# Clear current screen
		self.screen.fill(pygame.Color("black"))

		# Waiting room's layout
		waiting_room_wall_image = pygame.image.load(self.path+"MEDIA/waiting_room_wall.jpeg")
		self.screen.blit(waiting_room_wall_image, (0,0))

		# Player's record board
		player_icon_image = pygame.image.load(self.path+"MEDIA/player_icon.png")
		self.screen.blit(player_icon_image, (110,80))
		text_color = pygame.Color("white")
		text_font = pygame.font.SysFont("Calibri", 15, bold = True, italic = False)
		username_string = getpass.getuser()
		username_image = text_font.render(username_string, True, text_color)
		username_left_top = (180, 100)
		self.screen.blit(username_image, username_left_top)

		pygame.draw.line(self.screen, pygame.Color("white"), (110, 170), (390, 170), 2)
		solved_icon_image = pygame.image.load(self.path+"MEDIA/solved_icon.png")

		self.screen.blit(solved_icon_image, (110, 210))
		solved_prompt_string = f"Solved: {self.solved}"
		solved_prompt_image = text_font.render(solved_prompt_string, True, text_color)
		solved_prompt_left_top = (180, 230)
		self.screen.blit(solved_prompt_image, solved_prompt_left_top)
		
		quickest_case_icon_image = pygame.image.load(self.path+"MEDIA/quickest_case_icon.png")
		self.screen.blit(quickest_case_icon_image, (110, 290))
		quickest_case_prompt_string = f"Quickest Case: {self.quickest_case}"
		quickest_case_prompt_image = text_font.render(quickest_case_prompt_string, True, text_color)
		quickest_case_prompt_left_top = (180, 300)
		self.screen.blit(quickest_case_prompt_image, quickest_case_prompt_left_top)

		total_hours_icon_image = pygame.image.load(self.path+"MEDIA/total_hours_icon.png")
		self.screen.blit(total_hours_icon_image, (110, 370))
		total_hours_prompt_string = f"Total Time: {self.total_time} s"
		total_hours_prompt_image = text_font.render(total_hours_prompt_string, True, text_color)
		total_hours_prompt_left_top = (180, 380)
		self.screen.blit(total_hours_prompt_image, total_hours_prompt_left_top)
		
		skills_mastered_icon_image = pygame.image.load(self.path+"MEDIA/skills_mastered_icon.png")
		self.screen.blit(skills_mastered_icon_image, (110, 450))
		skills_mastered_prompt_string = f"Skills Mastered: {self.skills_mastered}"
		skills_mastered_prompt_image = text_font.render(skills_mastered_prompt_string, True, text_color)
		skills_mastered_prompt_left_top = (180, 460)
		self.screen.blit(skills_mastered_prompt_image, skills_mastered_prompt_left_top)

		# Doors to rooms
		if (self.screen.get_width()-130-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-130) and (110 <= pygame.mouse.get_pos()[1] <= (110+40)):
			door1_color = pygame.Color("black")
		else:
			door1_color = pygame.Color("grey")
		door1 = Button(self.screen, door1_color, self.screen.get_width()-130-155, 110, 155, 40, "Room 1")
		door1.draw()

		if (self.screen.get_width()-130-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-130) and (200 <= pygame.mouse.get_pos()[1] <= (200+40)):
			door2_color = pygame.Color("black")
		else:
			door2_color = pygame.Color("grey")
		door2 = Button(self.screen, door2_color, self.screen.get_width()-130-155, 200, 155, 40, "Room 2")
		door2.draw()

		pygame.draw.line(self.screen, pygame.Color("white"), (self.screen.get_width()-180-155, 350), (self.screen.get_width()-135, 350), 2)

		if (self.screen.get_width()-130-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-130) and (470 <= pygame.mouse.get_pos()[1] <= (470+40)):
			door5_color = pygame.Color("black")
		else:
			door5_color = pygame.Color("grey")
		door5 = Button(self.screen, door5_color, self.screen.get_width()-130-155, 470, 155, 40, "Tutorial Room")
		door5.draw()

		# Music control
		if (self.screen.get_width()-130-155 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-130) and (560 <= pygame.mouse.get_pos()[1] <= (560+40)):
			music_control_button_color = pygame.Color("grey")
		else:
			music_control_button_color = pygame.Color("black")
		if self.music_on:
			music_control_button_text = "Music Off"
		else:
			music_control_button_text = "Music On"
		music_control_button = Button(self.screen, music_control_button_color, self.screen.get_width()-130-155, 560, 155, 40, music_control_button_text)
		music_control_button.draw()

	def draw_exhibition_room(self):
		# Clear current room
		self.screen.fill(pygame.Color("black"))

		# Open exhibition book
		exhibition_book = pygame.image.load(self.path+"MEDIA/exhibition_book.png")
		self.screen.blit(exhibition_book, ((self.screen.get_width()//2)-(exhibition_book.get_width()//2), 20))
		if (800 <= pygame.mouse.get_pos()[0] <= 800+90) and (590 <= pygame.mouse.get_pos()[1] <= (590+40)):
			back_to_reception_button_color = pygame.Color("grey")
		else:
			back_to_reception_button_color = pygame.Color("black")
		back_to_reception_button = Button(self.screen, back_to_reception_button_color, 800, 590, 90, 40, "Go Back")
		back_to_reception_button.draw()

	def draw_room1(self):
		# Clear current room
		self.screen.fill(pygame.Color("black"))

		# Keep track of time in the room
		self.room_time_left = 600 - int(time.time() - self.room_start_time)
		time_string = "Time Left: " + str(self.room_time_left) + " seconds"
		time_color = pygame.Color("orange")
		time_font = pygame.font.SysFont("Calibri", 12, bold = True, italic = False)
		time_image = time_font.render(time_string, True, time_color)
		time_left_top = (10, 10)

		# Room 1's layout
		room1_layout = pygame.image.load(self.path+"MEDIA/room1_layout.png")
		self.screen.blit(room1_layout, (0,0))

		# Room 1's exit button
		if (0 <= pygame.mouse.get_pos()[0] <= 90) and (self.screen.get_height()-40 <= pygame.mouse.get_pos()[1] <= self.screen.get_height()):
			back_to_waiting_room_button_color = pygame.Color("black")
		else:
			back_to_waiting_room_button_color = pygame.Color("grey")
		back_to_waiting_room_button = Button(self.screen, back_to_waiting_room_button_color, 0, self.screen.get_height()-40, 90, 40, "Exit")
		back_to_waiting_room_button.draw()

		# Room 1's row 1's students and their bags
		col1_pos = 295
		row1_pos = 350
		for _ in range(5):
			student = pygame.image.load(self.path+"MEDIA/room1s_student.png")
			self.screen.blit(student, (col1_pos,row1_pos))
			bag = pygame.image.load(self.path+"MEDIA/student_bag.png")
			self.screen.blit(bag, (col1_pos+50, row1_pos))
			col1_pos += 160

		# Room 1's row 2's students and their bags
		col1_pos = 295
		row2_pos = 500
		for _ in range(5):
			student = pygame.image.load(self.path+"MEDIA/room1s_student.png")
			self.screen.blit(student, (col1_pos,row2_pos))
			bag = pygame.image.load(self.path+"MEDIA/student_bag.png")
			self.screen.blit(bag, (col1_pos+50, row2_pos))
			col1_pos += 160

		# Draw students' inner thoughts
		if not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			if 515 <= self.room_time_left <= 520:
				jp2s_distraction1 = pygame.image.load(self.path+"MEDIA/jp2s_distraction1.png")
				self.screen.blit(jp2s_distraction1, (210, 280))
			if  540 <= self.room_time_left <= 545:
				jps_distraction1 = pygame.image.load(self.path+"MEDIA/jps_distraction1.png")
				self.screen.blit(jps_distraction1, (295+160*4+40+26, 350-60))
			if 385 <= self.room_time_left <= 390:
				jps_distraction2 = pygame.image.load(self.path+"MEDIA/jps_distraction2.png")
				self.screen.blit(jps_distraction2, (295+160*4+40+26, 350-60))
			if 340 <= self.room_time_left <= 345:
				jp2s_distraction2 = pygame.image.load(self.path+"MEDIA/jp2s_distraction2.png")
				self.screen.blit(jp2s_distraction1, (210, 280))

		# Room 1's row 1's lunch boxes
		col1_pos = 290
		row1_pos = 300
		for _ in range(4):
			if 450 <= self.room_time_left <= 500 and not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
				item = pygame.image.load(self.path+"MEDIA/room1s_lunch_box.png")
			else:
				item = pygame.image.load(self.path+"MEDIA/room1s_table.png")
			self.screen.blit(item, (col1_pos,row1_pos))
			col1_pos += 160
		if 400 <= self.room_time_left <= 500 and not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			john_pauls_item = pygame.image.load(self.path+"MEDIA/room1s_lunch_box.png")
		else:
			john_pauls_item = pygame.image.load(self.path+"MEDIA/room1s_table.png")
		self.screen.blit(john_pauls_item, (col1_pos,row1_pos))

		# Room 2's row 2's lunch boxes
		col1_pos = 290
		row2_pos = 450
		for _ in range(4):
			if 450 <= self.room_time_left <= 500 and not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
				item = pygame.image.load(self.path+"MEDIA/room1s_lunch_box.png")
			else:
				item = pygame.image.load(self.path+"MEDIA/room1s_table.png")
			self.screen.blit(item, (col1_pos,row2_pos))
			col1_pos += 160
		if 480 <= self.room_time_left <= 500 and not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			tunley_roberts_item = pygame.image.load(self.path+"MEDIA/room1s_spoiled_lunch_box.png")
		else:
			tunley_roberts_item = pygame.image.load(self.path+"MEDIA/room1s_table.png")
		self.screen.blit(tunley_roberts_item, (col1_pos, row2_pos))

		# Doctor's note on the floor
		targets_doctors_note = pygame.image.load(self.path+"MEDIA/targets_doctors_note.png")
		self.screen.blit(targets_doctors_note, (self.screen.get_width()-40, self.screen.get_height()-40))
		
		# Room 1's answers board
		names_board = pygame.image.load(self.path+"MEDIA/names_board.png")
		self.screen.blit(names_board, ((self.screen.get_width()//2)-(names_board.get_width()//2), 12))
		
		# Teacher
		teacher = Moving_Person(self.screen, self.teacher_pos, self.path+"MEDIA/room1s_teacher.png", self.teacher_velocity)
		teacher.draw()
		if not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			if 579 <= self.room_time_left <= 585 and self.teacher_pos[0] < 600+330:
				teacher.move()
			if 569 <= self.room_time_left <= 577:
				teachers_message = pygame.image.load(self.path+"MEDIA/teachers_message.png")
				self.screen.blit(teachers_message, (self.teacher_pos[0]-80, 70))
			if self.room_time_left == 567:
				self.teacher_velocity = [-3,0]
			if 559 <= self.room_time_left <= 565 and self.teacher_pos[0] > 600:
				teacher.move()
			if self.room_time_left == 252:
				self.teacher_velocity = [2,-3]
			if 244 <= self.room_time_left <= 250 and self.teacher_pos != [800, 40]:
				teacher.move()

		# Open and close bags
		if not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			if self.room1_bag1_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/jp2_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag2_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/js_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag3_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/js2_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag4_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/kd_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag5_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/jp_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag6_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/lm_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag7_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/ph_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag8_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/ce_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag9_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/hq_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_bag10_opened:
				items_in_bag = pygame.image.load(self.path+"MEDIA/tr_bag_items.png")
				self.screen.blit(items_in_bag, ((self.screen.get_width()//2)-(items_in_bag.get_width()//2), (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
				close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(items_in_bag.get_width()//2)+30, (self.screen.get_height()//2)-(items_in_bag.get_height()//2)))
			elif self.room1_targets_doctors_note_opened:
				note = pygame.image.load(self.path+"MEDIA/targets_doctors_note_full_size.png")
				self.screen.blit(note, ((self.screen.get_width()//2)-(note.get_width()//2), (self.screen.get_height()//2)-(note.get_height()//2)))
				close_note_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
				self.screen.blit(close_note_icon, ((self.screen.get_width()//2)+(note.get_width()//2)+30, (self.screen.get_height()//2)-(note.get_height()//2)))
		
		# Room 1's final message
		message_board = pygame.Rect((self.screen.get_width()//2)-250, (self.screen.get_height()//2)-150, 500, 300)
		if not self.room1_wrong_answer_picked:
			message = "Mission complete! You found the victim."
		else:
			message = "Mission failed! Better luck next time."
		message_color = pygame.Color("white")
		message_font = pygame.font.SysFont("Calibri", 16, bold = True, italic = False)
		message_image = message_font.render(message, True, message_color)
		message_left_top = ((self.screen.get_width()//2)-(message_image.get_width()//2), (self.screen.get_height()//2)-(message_image.get_height()//2))
		
		# Room 1's clock
		if self.room_time_left >= 0 and not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			self.screen.blit(time_image, time_left_top)
		else:
			self.room1s_solution_button_on = True
			pygame.draw.rect(self.screen, pygame.Color("black"), message_board)
			self.screen.blit(message_image, message_left_top)
			see_solution_button = Button(self.screen, pygame.Color("grey"), self.screen.get_width()//2 - 60, 430, 120, 40, "See Solution")
			see_solution_button.draw()
		
		# Room 1's solution
		if self.room1s_solution_on:
			solution = pygame.image.load(self.path+"MEDIA/room1s_solution.png")
			self.screen.blit(solution, (self.screen.get_width()//2-solution.get_width()//2, self.screen.get_height()//2-solution.get_height()//2))
			close_bag_icon = pygame.image.load(self.path+"MEDIA/close_bag_icon.png")
			self.screen.blit(close_bag_icon, ((self.screen.get_width()//2)+(solution.get_width()//2)+30, (self.screen.get_height()//2)-(solution.get_height()//2)))
		
		# Room 1's signs revision
		if self.room1s_signs_opened:
			signs = pygame.image.load(self.path+"MEDIA/room1s_signs.png")
			self.screen.blit(signs, (self.screen.get_width()//2-signs.get_width()//2, self.screen.get_height()//2-signs.get_height()//2))

		# Keep track of room 1's status
		if 400 <= self.room_time_left <= 500 and not self.room1_john_paul_picked and not self.room1_wrong_answer_picked:
			status = "Status: Lunch Time"
		else:
			status = "Status: Studying Time"
		status_color = pygame.Color("orange")
		status_font = pygame.font.SysFont("Calibri", 12, bold = True, italic = False)
		status_image = status_font.render(status, True, status_color)
		status_left_top = (10, 30)
		self.screen.blit(status_image, status_left_top)

	def draw_room2(self):
		# Clear the screen
		self.screen.fill(pygame.Color("black"))

		# Keep track of time in room 2
		self.room_time_left = 600 - int(time.time() - self.room_start_time)
		time_string = "Time Left: " + str(self.room_time_left) + " seconds"
		time_color = pygame.Color("grey")
		time_font = pygame.font.SysFont("Calibri", 12, bold = True, italic = False)
		time_image = time_font.render(time_string, True, time_color)
		time_left_top = (self.screen.get_width()-90-30-100-30-time_image.get_width(), self.screen.get_height()-10-time_image.get_height())

		# Build layout
		room2_layout = pygame.image.load(self.path+"MEDIA/room2_layout.png")
		self.screen.blit(room2_layout, (0,0))

		# Show exit and answer buttons
		if (self.screen.get_width()-90 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()) and (self.screen.get_height()-40 <= pygame.mouse.get_pos()[1] <= self.screen.get_height()):
			back_to_waiting_room_button_color = pygame.Color("black")
		else:
			back_to_waiting_room_button_color = pygame.Color("grey")
		back_to_waiting_room_button = Button(self.screen, back_to_waiting_room_button_color, self.screen.get_width()-90, self.screen.get_height()-40, 90, 40, "Exit")
		back_to_waiting_room_button.draw()

		if (self.screen.get_width()-90-30-100 <= pygame.mouse.get_pos()[0] <= self.screen.get_width()-90-30) and (self.screen.get_height()-40 <= pygame.mouse.get_pos()[1] <= self.screen.get_height()):
			answer_button_color = pygame.Color("black")
		else:
			answer_button_color = pygame.Color("grey")
		answer_button = Button(self.screen, answer_button_color, self.screen.get_width()-90-30-100, self.screen.get_height()-40, 100, 40, "Answer")
		answer_button.draw()

		if len(self.letters_pressed) < 11:
			if not self.room2s_answer_button_pressed:
				# Open the journal
				if self.room2s_journal_opened:
					journal = pygame.image.load(self.path+"MEDIA/room2s_journal.png")
					self.screen.blit(journal, (self.screen.get_width()//2-journal.get_width()//2, self.screen.get_height()//2-journal.get_height()//2))

				# Open the phone
				if self.room2s_phone_opened:
					phone = pygame.image.load(self.path+"MEDIA/room2s_phone.png")
					self.screen.blit(phone, (self.screen.get_width()//2-phone.get_width()//2, self.screen.get_height()//2-phone.get_height()//2))

				# Open the suitcase
				if self.room2s_suitcase_opened:
					suitcase = pygame.image.load(self.path+"MEDIA/room2s_suitcase.png")
					self.screen.blit(suitcase, (self.screen.get_width()//2-suitcase.get_width()//2, self.screen.get_height()//2-suitcase.get_height()//2))

				# Open the note
				if self.room2s_note_opened:
					note = pygame.image.load(self.path+"MEDIA/room2s_note.png")
					self.screen.blit(note, (self.screen.get_width()//2-note.get_width()//2, self.screen.get_height()//2-note.get_height()//2))

				# Open the bottle
				if self.room2s_water_bottle_opened:
					water_bottle = pygame.image.load(self.path+"MEDIA/room2s_water_bottle.png")
					self.screen.blit(water_bottle, (self.screen.get_width()//2-water_bottle.get_width()//2, self.screen.get_height()//2-water_bottle.get_height()//2))

				# Open the box
				if self.room2s_box_opened:
					box = pygame.image.load(self.path+"MEDIA/room2s_box.png")
					self.screen.blit(box, (self.screen.get_width()//2-box.get_width()//2, self.screen.get_height()//2-box.get_height()//2))

			# Room 2's answer keyboard
			else:
				keyboard = pygame.image.load(self.path+"MEDIA/room2s_keyboard.png")
				self.screen.blit(keyboard, (self.screen.get_width()//2-keyboard.get_width()//2, self.screen.get_height()//2-keyboard.get_height()//2))
				keyscreen = pygame.image.load(self.path+"MEDIA/room2s_keyscreen.png")
				self.screen.blit(keyscreen, (self.screen.get_width()//2-keyscreen.get_width()//2, self.screen.get_height()//2-keyboard.get_height()//2 - 70 - 50))

				# Take and show player's inputs
				if self.room2s_spaces_filled <= 11:
					left = 319
					for letter in self.letters_pressed:
						letter_color = pygame.Color("red")
						letter_font = pygame.font.SysFont("Calibri", 40, bold = True, italic = True)
						letter_image = letter_font.render(letter, True, letter_color)	
						letter_left_top = (left, 200)
						self.screen.blit(letter_image, letter_left_top)
						left += 51
		else:
			self.room2s_answer_button_pressed = False
			# Congratulation message
			if self.letters_pressed == ["J","A","Y","D","E","N","S","M","I","T","H"]:
				congratulation = pygame.image.load(self.path+"MEDIA/room2s_congratulation.png")
				self.screen.blit(congratulation, (self.screen.get_width()//2-congratulation.get_width()//2, self.screen.get_height()//2-congratulation.get_height()//2))
			# Failure feedback
			else:
				failure = pygame.image.load(self.path+"MEDIA/room2s_failure.png")
				self.screen.blit(failure, (self.screen.get_width()//2-failure.get_width()//2, self.screen.get_height()//2-failure.get_height()//2))
			
			if self.room2s_solution_on:
				solution = pygame.image.load(self.path+"MEDIA/room2s_solution.png")
				self.screen.blit(solution, (self.screen.get_width()//2-solution.get_width()//2, self.screen.get_height()//2-solution.get_height()//2))

			if self.room2s_signs_opened:
				signs = pygame.image.load(self.path+"MEDIA/room2s_signs.png")
				self.screen.blit(signs, (self.screen.get_width()//2-signs.get_width()//2, self.screen.get_height()//2-signs.get_height()//2))

		# Room 2's clock
		if self.room_time_left >= 0:
			self.screen.blit(time_image, time_left_top)

	def find_letter_pressed(self, pos):
		if (316 <= pos[0] <= 316+50) and (297 <= pos[1] <= 297+50):
			letter = "A"
		elif (316+52 <= pos[0] <= 316+50*2) and (297 <= pos[1] <= 297+50):
			letter = "B"
		elif (316+50*2+2 <= pos[0] <= 316+50*3) and (297 <= pos[1] <= 297+50):
			letter = "C"
		elif (316+50*3+2 <= pos[0] <= 316+50*4) and (297 <= pos[1] <= 297+50):
			letter = "D"
		elif (316+50*4+2 <= pos[0] <= 316+50*5) and (297 <= pos[1] <= 297+50):
			letter = "E"
		elif (316+50*5+2 <= pos[0] <= 316+50*6) and (297 <= pos[1] <= 297+50):
			letter = "F"
		elif (316+50*6+2 <= pos[0] <= 316+50*7) and (297 <= pos[1] <= 297+50):
			letter = "G"
		elif (316+50*7+2 <= pos[0] <= 316+50*8) and (297 <= pos[1] <= 297+50):
			letter = "H"
		elif (316+50*8+2 <= pos[0] <= 316+50*9) and (297 <= pos[1] <= 297+50):
			letter = "I"
		elif (316+50*9+2 <= pos[0] <= 316+50*10) and (297 <= pos[1] <= 297+50):
			letter = "J"
		elif (316+50*10+2 <= pos[0] <= 316+50*11) and (297 <= pos[1] <= 297+50):
			letter = "K"
		elif (316+50*11+2 <= pos[0] <= 316+50*12) and (297 <= pos[1] <= 297+50):
			letter = "L"
		elif (316+50*12+2 <= pos[0] <= 316+50*13) and (297 <= pos[1] <= 297+50):
			letter = "M"
		elif (316 <= pos[0] <= 316+50) and (297+50 <= pos[1] <= 297+50+50):
			letter = "N"
		elif (316+52 <= pos[0] <= 316+50*2) and (297+50 <= pos[1] <= 297+50+50):
			letter = "O"
		elif (316+50*2+2 <= pos[0] <= 316+50*3) and (297+50 <= pos[1] <= 297+50+50):
			letter = "P"
		elif (316+50*3+2 <= pos[0] <= 316+50*4) and (297+50 <= pos[1] <= 297+50+50):
			letter = "Q"
		elif (316+50*4+2 <= pos[0] <= 316+50*5) and (297+50 <= pos[1] <= 297+50+50):
			letter = "R"
		elif (316+50*5+2 <= pos[0] <= 316+50*6) and (297+50 <= pos[1] <= 297+50+50):
			letter = "S"
		elif (316+50*6+2 <= pos[0] <= 316+50*7) and (297+50 <= pos[1] <= 297+50+50):
			letter = "T"
		elif (316+50*7+2 <= pos[0] <= 316+50*8) and (297+50 <= pos[1] <= 297+50+50):
			letter = "U"
		elif (316+50*8+2 <= pos[0] <= 316+50*9) and (297+50 <= pos[1] <= 297+50+50):
			letter = "V"
		elif (316+50*9+2 <= pos[0] <= 316+50*10) and (297+50 <= pos[1] <= 297+50+50):
			letter = "W"
		elif (316+50*10+2 <= pos[0] <= 316+50*11) and (297+50 <= pos[1] <= 297+50+50):
			letter = "X"
		elif (316+50*11+2 <= pos[0] <= 316+50*12) and (297+50 <= pos[1] <= 297+50+50):
			letter = "Y"
		elif (316+50*12+2 <= pos[0] <= 316+50*13) and (297+50 <= pos[1] <= 297+50+50):
			letter = "Z"

		return letter

	def draw_tutorial_room(self):
		# Clear the current screen
		self.screen.fill(pygame.Color("black"))

		# Tutorial book
		tutorial = pygame.image.load(self.path+"MEDIA/tutorial.png")
		self.screen.blit(tutorial, (0,0))

	def add_records(self, room, skills, time, solved):
		conn = sqlite3.connect(self.path+"DB_Files/GAME_RECORD.db")
		cursor = conn.cursor()
		sql_skills_update_query = f"""Update GAMER_RECORDS set SKILLS = {skills} where ROOM = {room}"""
		cursor.execute(sql_skills_update_query)
		sql_time_update_query = f"""Update GAMER_RECORDS set TIME = {time} where ROOM = {room}"""
		cursor.execute(sql_time_update_query)
		sql_solved_update_query = f"""Update GAMER_RECORDS set SOLVED = {solved} where ROOM = {room}"""
		cursor.execute(sql_solved_update_query)
		conn.commit()
		conn.close()
	
	def get_stats(self):
		conn = sqlite3.connect(self.path+"DB_Files/GAME_RECORD.db")
		cursor = conn.cursor()
		solved = 0
		total_time = 0
		quickest_case = "..."
		quickest_time = 600
		skills_mastered = 0
		cursor.execute("SELECT * FROM GAMER_RECORDS")
		rooms = cursor.fetchall()

		for room in rooms:
			if room[3] == 1:
				solved += 1

			total_time += room[2]
			
			if room[1]:
				skills_mastered += room[1]

			if room[2] != 0 and room[2] < quickest_time:
				quickest_time = room[2]
				quickest_case = room[0]
		conn.close()

		return [solved, quickest_case, total_time, skills_mastered]				
				
class Button:
	def __init__(self, screen, color, left, top, width, height, button_text):
		self.screen = screen
		self.color = color
		self.left = left
		self.top = top
		self.width = width
		self.height = height
		self.button_text = button_text
	
	def draw(self):
		button_image = pygame.Rect(self.left, self.top, self.width, self.height)
		pygame.draw.rect(self.screen, self.color, button_image)
		text_color = pygame.Color("white")
		text_font = pygame.font.SysFont("Calibri", 15, bold = True, italic = False)
		button_text_image = text_font.render(self.button_text, True, text_color)
		button_text_left_top = (self.left + (self.width//2)-(button_text_image.get_width()//2), self.top + (self.height//2) - (button_text_image.get_height()//2))
		self.screen.blit(button_text_image, button_text_left_top)

class Moving_Person:
	def __init__(self, screen, pos, image_src, velocity):
		self.screen = screen
		self.pos = pos
		self.image_src = image_src
		self.velocity = velocity
	
	def move(self):
		for index in range(2):
			self.pos[index] += self.velocity[index]

	def draw(self):
		moving_person = pygame.image.load(self.image_src)
		self.screen.blit(moving_person, self.pos)

main()	

