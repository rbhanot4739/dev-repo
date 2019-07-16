def first():
    def second():
        print("I am in second fxn")
        print("Thank you for calling me")

    print("I am first fxn and i am going to second fxn")
    second()


first()
