
print("\033[31m")
print("=" * 32)
print("      DEMON HEADSHOT PANEL")
print("=" * 32)
print("\033[0m")

print("1. Sensitivity Settings")
print("2. HUD Settings")
print("3. Fire Button Settings")
print("4. Exit")

choice = input("\nChoose option: ")

if choice == "1":
    print("\nSensitivity Settings")
    print("General: 190")
    print("Red Dot: 180")
    print("2x Scope: 170")
    print("4x Scope: 160")
elif choice == "2":
    print("\nHUD: Customize in game settings")
elif choice == "3":
    print("\nFire Button: Adjust to your comfort")
elif choice == "4":
    print("Bye, Demon!")
else:
    print("Invalid option!")

