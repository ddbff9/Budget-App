#********************************************************
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

    output = self.name.center(30, "*") + "\n"
    for item in self.ledger:
      output += f"{item['description'][:23].ljust(23)}{format(item['amount'],'.2f').rjust(7)}\n"
    output += f"Total: {format(self.get_balance(),'.2f')}"
    return output

  #Ensures that an overdraft doesn't occur.
  def check_funds(self, amount):
    if amount <= self.get_balance():
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
  
#********************************************************

def create_spend_chart(categories):
  category_names = []
  spent = []
  spent_percentages = []

  for category in categories:
    total = 0
    for item in category.ledger:
      if item['amount'] < 0:
        total -= item['amount']
    spent.append(round(total, 2))
    category_names.append(category.name)

  for amount in spent:
    spent_percentages.append(round(amount / sum(spent), 2)*100)

  graph = "Percentage spent by category\n"

  labels = range(100, -10, -10)


  for label in labels:
    graph += str(label).rjust(3) + "| "
    for percent in spent_percentages:
      if percent >= label:
        graph += "o  "
      else:
        graph += "   "
    graph += "\n"

  graph += "    ----" + ("---" * (len(category_names) - 1))
  graph += "\n     "

  longest_name_length = 0

  for name in category_names:
    if longest_name_length < len(name):
      longest_name_length = len(name)

  for i in range(longest_name_length):
    for name in category_names:
      if len(name) > i:
        graph += name[i] + "  "
      else:
        graph += "   "
    if i < longest_name_length-1:
      graph += "\n     "

  return graph