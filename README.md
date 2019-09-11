# WorldCreator
Welcome to my first public project for Python. This work was spawned of a need for a particular type of world-building program and is intended to be used as a reference tool/creativity tool before, during and after games of D&D. While designed with D&D in mind I left it "fairly" open ended as to how you'd like to create your world. 

This project utilizes PySide2 for it's GUI. The command line commandusing pip to install this package on Windows (The machine I use) is as follows.

pip install PySide2

Troubleshooting can be found here - https://packaging.python.org/tutorials/installing-packages/

While I'm fairly certain in it's current state it's workable.

As for a few acknowledgements;
My older brother ChaoticSeven who got me into DMing and when he heard about this tool he pushed me and pushed me into finishing it, or at least getting it to somewhere he could play around with it. 
My good friend Hill, he likes hills. He likes climbing and then claiming hills as his own, and he hates radios. Regardless, I got him into D&D and now he can't get enough of it. He heard about this tool and unendingly gives me new features to add into it. He has no idea what goes into all of this, but his idea's are great nonetheless.

Below is a quick tutorial to using the piece of software because as a self-learned programmer I obviously have some wack control schemes for this thing.

When run a console should remain open in the background. This is for error reporting, you don't need to mind it at all unless something weird happens. If such a thing occurs, check for an error. Lack of an error showing doesn't mean that there isn't as mistake though, Python has a tendancy to skip over somethings and try to keep working anyway. 

The first window that shows up is your main window. You'll need to create a country by typing a name and clicking the button. From there you can create a landscape. 

Landscapes will always be underneath the country, never anything else. If you make more landscapes they will be created under the currently selected country, always. 

From here if you select the landscape and then go to change the type of feature, you'll see there are new choices. This box updates everytime you switch features, into what you can create underneath that feature. Landscape will always be an option. 

If you double click on anything (Country or Feature) you will get an extended box. Landscapes are a bit special in that they also have a climate box. Type into the Add Climate Attribute box, and hit the Enter key when done to add it to the box to the left. Double click an attribute to remove it. You can add a description here as well, which will be remembered whenever the contents of the box is changed. 

The name is also changeable here, type the desired new name, and hit enter. The name will change. 

Images can be added to each country/feature. They are saved via image location, if the image name is changed, or moved it may not show up upon a future load. I reccomend keeping images within a folder in the same level as the worldcreator.py (or the executable).

The relationship system is last, you can add a relationship from one feature/country to another feature/country, but it will not make one the other way. ex. Country A makes a relationship with Country B. Country A will show the relationship, but Country B will not. You'll have to manually make a second one with Country B -> Country A. 

Select the relationship from the list in the Show Relationships window and then you'll be able to change a description of the relationship to the right. Again, it remembers as the contents are changed. You still have to save the file in order for them to be loaded. 

You can double click any relationship to open up the description-window for that feature/country as well (provided it's not already open)

I think that's about it! If there is any confusion you can email me at 7heDubz@gmail.com, you can also reach me there with any errors/bugs you find so I might try to fix them. I would appreciate as much information about the issue as possible, including a screenshot of the error code (if there was one)
