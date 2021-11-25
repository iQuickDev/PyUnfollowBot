from selenium import webdriver
from time import sleep
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

f = open('config.txt', 'r')
config = f.read().splitlines()
f.close()

username = config[0].replace('username: "', "")[:-1]
password = config[1].replace('password: "', "")[:-1]
iteration_count = config[2].replace('iteration_count: ', "")
cycle_unfollow_count = config[3].replace('cycle_unfollow_count: ', "")
iteration_delay = config[4].replace('iteration_delay: ', "")
cycle_delay = config[5].replace('cycle_delay: ', "")

if (username == "un" or password == "pw"):
    print("Credentials to login have not been found, login manually")
    username = input("Username: ")
    password = input("Password: ")
    save = input("Would you like to save the credentials ? (y/n): ")

    if (save == "y"):
        f = open('config.txt', 'w')
        f.write('username: "' + username + '"\n')
        f.write('password: "' + password + '"\n')
        f.write('iteration_count: ' + iteration_count + '\n')
        f.write('cycle_unfollow_count: ' + cycle_unfollow_count + '\n')
        f.write('iteration_delay: ' + iteration_delay + '\n')
        f.write('cycle_delay: ' + cycle_delay + '\n')
        f.close()

execution_time_in_seconds = int(iteration_count) * int(cycle_unfollow_count) * int(iteration_delay) + int(cycle_delay)
total_accounts_to_unfollow = int(iteration_count) * int(cycle_unfollow_count)

print("The script has been initialized")
print("Total accounts to unfollow: " + str(total_accounts_to_unfollow))
print("Estimated execution time: about " + str(round(execution_time_in_seconds / 60, 1)) + " minutes")

driver = webdriver.Chrome()
driver.get('https://instagram.com')

print("[!] Connected to instagram.com")

sleep(2)

driver.find_element_by_xpath('//button[text()="Accept All"]').click()
print("[!] Accepted cookies")

sleep(2)

driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
driver.find_element_by_xpath("//input[@name='password']").send_keys(password)

driver.find_element_by_xpath("//button[@type='submit']").click()

print("[!] Entered credentials")

sleep(5)

driver.get('https://instagram.com/' + username + '/')

driver.find_element_by_partial_link_text("following").click()

print('[!] Opened "following" list')

sleep(3)

unfollowed_count = 0

for i in range(int(iteration_count)):
    print("----- Iteration #" + str(i) + " -----")
    for j in range(int(cycle_unfollow_count)):
        driver.find_element_by_xpath('//button[text()="Following"]').click()
        driver.find_element_by_xpath('//button[text()="Unfollow"]').click()
        unfollowed_count += 1
        unfollowed_account = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/ul/div/li[" + str(unfollowed_count) + "]/div/div[2]/div[1]/div/div/span/a").get_attribute("innerHTML")
        print("[" + str(unfollowed_count) + "] Unfollowed " + unfollowed_account)
        sleep(int(cycle_delay))
    sleep(int(iteration_delay))
