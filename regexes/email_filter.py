import re, string, random


def rand_letter_string(n=3):
    a = []
    for _ in range(n):
        a.extend(string.ascii_lowercase[random.randint(0, 24)])
    return ''.join(a)


# generate test data
set_size_small = 10
set_size_large = 50

test_vu_emails = []
test_vunet_ids = []
test_nonvunet_id_emails = []

for r in range(set_size_small):
    test_vu_emails.append(
        '{}{}@vu.nl'.format(rand_letter_string(3), random.randint(100, 999))
    )
for r in range(set_size_small):
    test_vu_emails.append('{}@vu.nl'.format(rand_letter_string(10)))
for r in range(set_size_small):
    test_vunet_ids.append(
        '{}{}'.format(rand_letter_string(3), random.randint(100, 999))
    )
for r in range(set_size_large):
    test_nonvunet_id_emails.append(
        '{}{}@{}.{}.{}'.format(
            rand_letter_string(3),
            random.randint(100, 999),
            rand_letter_string(10),
            rand_letter_string(10),
            rand_letter_string(2),
        )
    )

# pathalogical cases
test_nonvunet_id_emails.insert(0, 'abc900@vu.nl.com')

# print(test_vu_emails)
# print(test_vunet_ids)
# print(test_nonvunet_id_emails)


# regex

no_vu_email_1 = '^[a-z]{3}[0-9]{3}$|^(?![a-z]{3}[0-9]{3}\@vu\.nl$)'
no_vu_email_2 = '^[a-z]{3}[0-9]{3}$|^(?!\w*\@vu\.nl$)'  # brett
no_vu_email_3 = '^([a-z]{3}[0-9]{3}|.+@(?!vu\.nl).+\..+)$'  # peter


nve = re.compile(no_vu_email_3)

for pid in test_vunet_ids:
    r = re.match(nve, pid)
    print('{}: {}'.format(pid, r is not None))
print('\n')
for pid in test_vu_emails:
    r = re.match(nve, pid)
    print('{}: {}'.format(pid, r is not None))
print('\n')
for pid in test_nonvunet_id_emails:
    r = re.match(nve, pid)
    print('{}: {}'.format(pid, r is not None))
