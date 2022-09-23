# Detection of ships with dragged anchors

![ship drag](https://user-images.githubusercontent.com/38955297/191911126-c872819a-04fc-4f63-a9a2-8572a602c819.jpg)


## Problem statement: 
- A “dragging anchor” means the ship drifts without holding power even though it has been anchored. This can lead to less or more serious incidents, as collisions, groundings or strandings
- Power cable between Bornholm, Denmark and Sweden was hit by dragged anchor at 26th February 2022. The vessel name was “Samus swan”
- The damage done was worth millions of euros.

## Objective:
To develop an algorithm that can detect if a ship is dragging its anchor based on real-time AIS data
This can provide an early warning system and can prevent from accidents and huge losses.

## Algorithm:

1. Tt was observed that the AIS data of the ships with dragged anchor (ship name: SAMUS SWAN) were showing high frequency variation on the heading of the ship. 

    - Heading is the direction in which a vehicle/vessel is pointing at any given moment. It is expressed as the angular distance relative to north, usually 000° at north, clockwise through 359°, in degrees of either true, magnetic, or compass direction

<img src="https://user-images.githubusercontent.com/38955297/191911558-18d103d0-4f22-4ba4-960a-9cd265530d9d.jpg" height =300/>

2. Algorithm was developed to identify these motion in the heading AIS data of ships. 

    - Showing heading variation of ships on map: 
   
   ![heading variation of the ships on map](https://user-images.githubusercontent.com/38955297/191911847-76a9779b-8da3-477d-906b-694e4535bab9.png)
    
    you can observe the zig zag motion shown by the ship which was dragging anchor

    - Showing the heading variation profile on time scale:
    
    ![heading variation of the ships](https://user-images.githubusercontent.com/38955297/191911912-4294f1c6-b052-4882-b02c-322f2840cbf4.png)

3. Algorithm results: 

Ship that was dragging its anchor:

![result1](https://user-images.githubusercontent.com/38955297/191911963-f40de701-5074-42cb-a15e-e8d8977b6cbe.png)

Ship that wasn't dragging its anchor:

![result2](https://user-images.githubusercontent.com/38955297/191911995-f2fced0c-754b-493f-a897-a9248009298c.PNG)

A score was defined which is the fraction of zig-zag motion on heading data detected by the algorithm
