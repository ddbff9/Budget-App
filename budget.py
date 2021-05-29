class Category:

  #Method to determine how many stars are needed in title of category report.
  @staticmethod
  def get_stars(self):
    return (30 - len(self.name))//2

  #Method to initialize Category Class
  def __init__(self, name):
    self.name = name  
    self.ledger = []    # creates a new empty ledger for each category
    self.balance = 0    # Sets balance of category to $0

  #Method that will print out the budget report when Cateogry name is called.
  def __str__(self):
      line_list = []
 
    #Cleans up ledger entries to print out a budget report.
    #******************************************************

      for x in range(len(self.ledger)):
        
        #Splits each line in the ledger.
        line = str(self.ledger[x]).split("'")
        
        #Cleans up the description.
        desc = line[5].strip("','}")

        #Limits printing description out to only 23 characters.
        short_desc = desc[:23]

        #Cleans up the amount.
        amt = line[2].strip(",:, ")

        #Formats amount to display to two decimal places.
        amt = "{:.2f}".format(float(amt))
      
      #Creates a list of lines to report for category.
      #***********************************************

        #Calculates the number of spaces needed to make the line 30 characters long.
        space_len = 30 - len(short_desc) - len(amt)
        
        #Concatenates the description and amount into a 30 character line.
        whole_line = str(short_desc) + " " * space_len + str(amt)
        
        #Appends the line_list with the whole line entry.
        line_list.append(whole_line)
      
    #Creates budget report for category
    #**********************************

      #Creates the Title Row ***********Category***********
      title = "*" * Category.get_stars(self) + self.name + "*" * Category.get_stars(self)

      #Joins all lines in line_list for the Category budget report.
      lines = "\n".join(line_list)

      #Creates the Total amount for the Category budget report.
      total_line = "Total: " + str(self.balance)

      return  str(title) + "\n" + lines + "\n" + total_line

  #Ensures that an overdraft doesn't occur.
  def check_funds(self, amount):
    if self.balance - amount >=0:
      return True
    else:
      return False

  #Enters a depsoit into the category ledger.
  def deposit(self, amount, description=""):
      self.ledger.append({"amount":amount,"description":description})
      self.balance += amount

  #Enters a withdraw into the category ledger.
  def withdraw(self, amount, description=""): 
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      self.balance -= amount
      return True
    else:
      return False  
  
  def transfer(self, amount, category):
    
    if self.check_funds(amount):
      try:
        self.ledger.append({"amount": -amount, "description": f"Transfer to {category.name}"})
        self.balance -= amount
      except:
        self.ledger.append({"amount": -amount, "description": f"Transfer to {category}"})
        self.balance -= amount
    
      try:
        globals()[str(category).lower()].deposit(amount,f"Transfer from {self.name}")
      except:
        category.deposit(amount,f"Transfer from {self.name}")
      
      return True
    else:
      return False

  

  #Returns budget category balance when called.
  def get_balance(self):
    return self.balance
  
  try:
    def create_spend_chart(categories):
      pass
  except:
    "Not ready yet"



  
  

# food = Category("Food")
# entertainment = Category("Entertainment")

# food.deposit(1000,"initial deposit")
# food.withdraw(10.15,"groceries")
# food.withdraw(15.89,"restaurant and more food dont you know")
# food.transfer(50,"Entertainment")
# food.transfer(100,entertainment)
# print(str(food))
# print(str(entertainment))


