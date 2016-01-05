import random
import os
import sys

print("Hello Python")

name = "Matija"

print("Hello",name)

quote = "\"Always remember you are unique"

multi_line_quote = ''' just
like everyone else'''

new_string = quote + multi_line_quote

print("%s %s %s" % ('I like the quote', quote, multi_line_quote))

print('\n' * 5)

print("I don't like ", end="")
print("newlines")


# Lists

grocery_list = ['Juice', 'Tomatoes', 'Potatoes',
                'Bananas']
print('First item', grocery_list[0])
grocery_list[0] = 'Green Juice'
print('First item', grocery_list[0])

print(grocery_list[1:3])

other_events = ['Wash car', 'Pick up kids', 'Cash check']
to_do_list = [other_events, grocery_list]
print(to_do_list)
print(to_do_list[1][1])

grocery_list.append('Onions')
print(to_do_list)

grocery_list.sort()
print(grocery_list)

del grocery_list[1]
print(to_do_list)

to_do_list2 = other_events + grocery_list
print(len(to_do_list2))
print(max(to_do_list2))
print(min(to_do_list2))


# Tuples

pi_tuple = (3, 1, 4, 1, 5, 9)
print(pi_tuple)

new_list = list(pi_tuple)
print(new_list)

new_tuple = tuple(new_list)
print(new_tuple)
print(len(new_tuple))
print(max(new_tuple))
print(min(new_tuple))


# Dictionaries

super_villains = {'Fiddler' : 'Isaac Bowin',
                  'Captain Cold' : 'Leonard Snart',
                  'Weather Wizard' : 'Mark Mardon',
                  'Mirror Master' : 'Sam Scudder',
                  'Pied Piper' : 'Thomas Peterson'
                  }

print(super_villains['Captain Cold'])

del super_villains['Fiddler']

super_villains['Pied Piper'] = 'Hartley Rathaway'
print(super_villains.get("Pied Piper"))

print(super_villains)
print(len(super_villains))
print(max(super_villains))
print(min(super_villains))

print(super_villains.keys())
print(super_villains.values())


# Conditionals

def can_drive(age):
    if age > 16 :
        print('You are old enough to drive')
    else :
        print('You are not old enough to drive')

can_drive(21)
can_drive(14)

def is_teen(age):
    if (age >= 13 and age <= 19):
        print("You are teen at the age of", age)
    else:
        print("You are not teen at the age of", age)

is_teen(12)
is_teen(13)
is_teen(18)
is_teen(20)


# Looping

for x in range(0, 10):
    print(x, ' ', end="")
print('\n')

for y in grocery_list:
    print(y)

for x in [2, 4, 6, 8, 10]:
    print(x)

for x in to_do_list:
    for y in x:
        print(y)

num_list = [[1,2,3], [10,20,30], [100,200,300]]
for x in range(0,3):
    for y in range(0,3):
        print(num_list[x][y])

random_number = random.randrange(0, 100)

# while random_number != 15:
#     print(random_number)
#     random_number = random.randrange(0, 100)

i = 0

while i <= 20:
    if i%2 == 0: print(i)
    i += 1


# Functions

def add_number(x, y):
    sum = x + y
    return sum

print(add_number(1,4))

#print("What is your name?")
#name = sys.stdin.readline()
#print("Hello",name)


# Strings

long_string = "I'll catch you if you fall - The Floor"
print(long_string[0:4])
print(long_string[-5:])
print(long_string[:-5])
print(long_string[:4] + " be there")

print("%c is my %s letter and my number %d number is %.5f" %
      ('X', 'favorite', 1, .14))

print(long_string.capitalize())
print(long_string.find("Floor"))
print(long_string.isalpha())
print(long_string.isalnum())
print(len(long_string))
print(long_string.replace("Floor", "Ground"))
print(long_string.strip())

quote_list = long_string.split(" ")
print(quote_list)


# File operations

test_file = open("test.txt", "wb")

print(test_file.mode)

test_file.write(bytes("Write me to the file\n", "UTF-8"))

test_file.close()

test_file = open("test.txt", "r+")

text_in_file = test_file.read()
print(text_in_file)

os.remove("test.txt")


# Objects

from Animal import Animal

cat = Animal("Whiskers", 33, 10, "Meow")
print(cat.tostring())

from Animal import Dog

spot = Dog("Spot", 53, 27, "Ruff", "Derek")
print(spot.tostring())

class AnimalTesting:
    def get_type(self, animal):
        animal.get_type()

test_animals = AnimalTesting()
test_animals.get_type(cat)
test_animals.get_type(spot)

spot.multiple_sounds(4)
spot.multiple_sounds()


from driver.connection import *

conn = Connection()
c = conn.connect()
print(c)
conn.disconnect()














