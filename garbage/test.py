num = 5
lista = ['a', 'b', 'c', 'd','e','f','g','h','i','j','k','l','m','n']
for i in range(int(len(lista)/5)):
    for j in range(num):
        print(lista[j + num*i])
for j in range(int(len(lista)/5), len(lista)):
    print(lista[j])