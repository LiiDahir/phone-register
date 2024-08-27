import os,pickle
class Contact:
	def __init__(self) -> None:
		self.numbers = {}
		self.load_data()
	def get_path(self):
		return  os.path.dirname(os.path.abspath(__file__))+"/data.pkl"

	def load_data(self):
		data_file = self.get_path()
		if(os.path.exists(data_file)):
			with open(data_file,"rb") as f:
				self.numbers = pickle.load(f)
				self.check_status(1)
		else:
			self.write_data()
			self.check_status(1)

	def write_data(self):
		data_file = self.get_path()
		with open(data_file, "wb") as f:
			pickle.dump(self.numbers, f)

	def show(self):
		print("Contacts")
		for id,List in self.numbers.items():
			print(f"No : {id} Name : {List[0]} and phone number {List[1]} and gmail {List[2]}")

	def show_sp(self,matches):
		for id,List in matches:
			print(f"No : {id} Name : {List[0]} and phone number {List[1]} and gmail {List[2]}")
		self.check_status(2)

	def add(self):
		id = len(self.numbers)
		name = input("Enter the contact name :  ")
		while not self.check_name(name):
			name = input("Enter the correct name :  ")

		phone = input("Enter the contact phone number : ")
		while not self.check_number(phone):
			phone = input("Please Enter correct phone !. : ")

		gmail = input("Enter the contact gmail : ")
		while not self.check_gmail(gmail):
			gmail = input("Enter the correct gmail : ")


		matches = self.check_duplicate(phone)
		while len(matches)>0:
			print("this phone number is alredy exists.")
			self.show_sp(matches)

		self.numbers[id]=[name,phone,gmail]
		self.check_status()

	def check_duplicate(self,phone):
		return[(id,List) for id, List in self.numbers.items() if List[1] == phone]
	

	def check_number(self,phone):
		return int(phone)>610000000 and int(phone)<699999999
	
	def check_gmail(self,gmail):
		return not(gmail[0].isnumeric()) and gmail.find("@") != -1 and gmail.find(".") != -1

	def check_name(self,name):
		return self.check_each(name)
	
	def check_each(self,name):
		valows = ["a","e","i","o","u"]
		names = name.split(" ")
		if len(names)<=2:
			return False
		
		for name in names:
			if len(name)<=2:
				return False
			for index in range(0,len(name)-2):
				if name[index] == name[index+1] == name[index+2]:
					return False
				if name[index].lower() in valows and name[index+1].lower() in valows and name[index+1].lower() in valows :
					return False
				if name[index].lower() not in valows and name[index+1].lower() not in valows and name[index+2].lower() not in valows :
					return False
				
		return True
				
	def delete(self):
		self.show()
		id = input("Enter the contact id you delete : ")
		if id in self.numbers:
			del self.numbers[id]
			self.check_status()
		else:
			print("the number you want to delete is not found !.")
			self.check_status(2)

	def edit(self):
		self.show()
		data = []
		id = input("Enter the ID :")

		if id in self.numbers:
			data = self.numbers[id]
			if len(data) != 0:
				new_name = input("Enter the New Name :")
				phone = input("Enete the phone number : ")

				if new_name!="" and phone!="":
					self.numbers[id] = [new_name,phone]
				elif new_name == "" and phone != "":
					self.numbers[id] = [data[0],phone]
				elif new_name != "" and phone == "":
					self.numbers[id] = [new_name,data[1]]
			self.check_status()


	def check_status(self,num=0):
		self.write_data()
		if num == 0:
			self.show()
			status = input("Do you exist : (y/n) ")
			if status !="y":
				self.check_status(1)		
			else: exit()
		if num == 2:
			status = input("Do you exist : (y/n) ")
			if status !="y":
				self.check_status(1)		
			else: exit()
		else:status =num
		if status==1:
			os.system("clear")
			print("1. add new phone  ")
			print("2. Edit the phone ")
			print("3. Delete the phone  ")
			print("4. Search")
			print("5. Exit ")
			select = int(input("select of theme : "))
			if select == 1:
				self.add()
			elif select == 2:
				self.edit()
			elif select == 3 :
				self.delete()
			elif select == 4 :
				self.Search()
			elif select == 5:
				exit()

	def Search(self):
		target = input("Enter target : ").lower()
		matches = [ (id,data) for id,data in self.numbers.items() if target in id or target in data[0].lower() or target in data[1] or target in data[2]]
		self.show_sp(matches)

obj = Contact()	

