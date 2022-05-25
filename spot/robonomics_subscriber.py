import robonomicsinterface as RI

interface = RI.RobonomicsInterface()
subscriber = RI.Subscriber(interface, RI.SubEvent.NewLaunch, lambda x,y: print(x,y),
                           "4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j")
