import robonomicsinterface as RI



def robonomics_transaction_callback(data, launch_event_id):
    sender, recipient, _ = data

    print(launch_event_id)
    print(data)

interface = RI.RobonomicsInterface()
print("Robonomics subscriber starting...")
subscriber = RI.Subscriber(interface, RI.SubEvent.NewLaunch, robonomics_transaction_callback, "4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j")
