
Foraging is a whiteboard-based online collaboration system.

The main personas can be divided into two categories: facilitator and participant.
- The facilitator is the organizer and host of the collaboration, responsible for designing and controlling the entire facilitated session process.
- A participant is a person who participates in discussions and provides input in a facilitated session.
In a facilitated session, there is usually more than one participant, and there can be more than one facilitator.

The main requirements of the facilitator are as follows:
- Facilitate sessions
- Structure data generated during the facilitated session

Facilitated sessions are run in the following ways:
- A facilitated session can be run according to pre-designed steps
- During step execution, the interactive behavior of elements on the whiteboard is controlled by permissions
- Permissions includes: movable, editable, selectable, etc.
- In different steps, the same element may have different behaviors
- A well-designed step can be solidified into a playbook

Structural data is generated during the facilitated session, which is achieved in the following ways:
- Map information in structural data to UI elements.
   - Structural data column, corresponding to tag (provided by container), or a custom field editable by facilitator
   - The lines of structural data can have multiple visual incarnations on the whiteboard, such as data entry sticky note
- After the above corresponding relationship is established, the operation of UI is the operation of structured data. For example, dragging the visual avatar of a row of a structured data table into the container is equivalent to tagging the row of data

Structural data can be seen as the data shared by all facilitators in the facilitated session
- Facilitator can modify structured data at any time
- Structured data can be imported in batches by uploading csv files

There are three main categories of elements that can be used on the whiteboard:
- 1 is data sticky, every time a new data sticky is created, a row of corresponding data will be generated in the facilitator data table
- 2 is the container, the container is used to label the data, when a data sticky is moved into the container, the facilitator can collect the labeled structural data
- 3 is non-data sticky, its creation will not generate data in the data table, and after being moved into the container, it will not be associated with the container

Whiteboard-based collaboration
- Multiple participants collaborate on the whiteboard, and each other can see the latest modifications in real time
- Participants can add elements to the whiteboard to express their ideas
- Participants can move, rotate, stretch, create, delete elements, and modify the text on elements
- The operations of multiple participants on the whiteboard will converge into a single timeline. When undo/redo is, if the previous event of the same element on the timeline is not triggered by itself, it cannot be undo.
- Structural data can be imported in batches by uploading csv files

Delete behavior for whiteboard elements
- When the participant can delete any element on the whiteboard, if the deletion is successful, the element will disappear from the whiteboard
- When a participant deletes a data entry sticky note on the whiteboard, the element disappears from the whiteboard, but the corresponding data row in the facilitator data table will not be deleted
- When a participant deletes a container on the whiteboard, the element disappears from the whiteboard, and the tag corresponding to the data in the facilitator data table also disappears

Individual move behaviors for whiteboard elements
- Move a data sticky into the container, which means to tag the data, The data stiky will be associated with the container
- After the associated data sticky in a container is moved out of the container, the association between the data sticky and the container will be released
- Move a non-data sticky element into the container, which is not associated with the container
- When moving a container, the associated data sticky in the container will move with the container


Multi-select behavior for whiteboard elements
- Participant can select multiple data sticky in the same container at the same time
- The participant can select the container and other elements on the whiteboard outside the container at the same time
- The participant cannot select the associated data sticky inside the container and elements outside the container at the same time
- The participant cannot select associated data sticky in different containers at the same time
-

Multi-select mobile behavior
- The premise that multiple elements can be moved at the same time is that the participant has successfully selected multiple elements at the same time
- When the multi-selected elements are all data sticky, the participant can move them into or out of the container together
- When the multi-selected element has both data sticky and non-data sticky, the participant cannot move the data sticky into the container

- 
