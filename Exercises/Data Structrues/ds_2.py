zoo = ('python', 'elephant', 'penguin')
print('zoo has', len(zoo), 'animals')

new_zoo = 'monkey', 'camel', zoo
print('new_zoo has', len(new_zoo), 'cages')

print(new_zoo)
print('brought from old zoo are', new_zoo[2])
print('last animal brought from old zoo is', new_zoo[2][2])
print('number of animals in new zoo:', len(new_zoo)+len(zoo)-1)
