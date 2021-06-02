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

  #Loops through categories and determines amount spen and category name and adds them to their respective lists.
  for category in categories:
    total = 0
    
    #Building total spent amount for that category, deposits don't count, thus looking for amounts < $0.
    for item in category.ledger:
      if item['amount'] < 0:
        total -= item['amount']
    
    #adds total spent to spent list and rounds output to two decimals.
    spent.append(round(total, 2))

    #Appends category name list with the name of the category.
    category_names.append(category.name)

  #Loops through the amounts in the spent list and determines the % spent by category as a total.
  for amount in spent:
    spent_percentages.append(round(amount / sum(spent), 2)*100)

  #Create Title line for graph string. (graph string conintues and is addeded to in each function below.)
  graph = "Percentage spent by category\n"

  #Create labes for graph.
  labels = range(100, -10, -10) #range(start, stop[, step])

  #First for loop gets you on label row, then second (nested) for loop adds the appropriate "o" based on % spent.
  for label in labels:
    graph += str(label).rjust(3) + "| "
    
    for percent in spent_percentages:
      #This always rounds down so if percentage is 78%, which is not >= 80% the "o" is only addeded to the 70% and down labels.
      if percent >= label:
        graph += "o  "
      else:
        graph += "   "
    
    #This will create a new line at the end of the label row, so when the next loop starts its starting on a new line.
    graph += "\n"

  #Once all label rows have been filled by the above for loop,this line will add the dashes.
  graph += "    ----" + ("---" * (len(category_names) - 1))
  
  #Adds a new line after the dash row.
  graph += "\n     "

  longest_name_length = 0

  #Determines which category name is the longest.
  for name in category_names:
    if longest_name_length < len(name):
      longest_name_length = len(name)


  for i in range(longest_name_length): #range(stop), so in this case range stops at the length of the longest name.

    #prints the list of category names vertically.
    for name in category_names:
      #Category name has a value within the current value of i, if so print the name. This allows shorter names to have spaces added once the word has been fully printed.
      if len(name) > i:
        graph += name[i] + "  "
      else:
        graph += "   "
    
    #This ensures that a new line is not created after the last row is printed.
    if i < longest_name_length-1:
      graph += "\n     "

  return graph