from russian_names import RussianNames

def custumer_generate():
    rn = RussianNames(count=1, patronymic=False, transliterate=True)
    batch = rn.get_batch()
    for person in batch:
        result = str(person).split(' ')
        return result

if __name__ == "__main__":
    custumer_generate()