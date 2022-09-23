# Detection of ships with dragged anchors

<img src="ship drag.jpg"/>

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

<img src="https://www.researchgate.net/profile/Nurman-Firdaus/publication/335690857/figure/fig2/AS:801122759503873@1568013958317/Definition-of-heading-angle-of-ship-against-wave.ppm" height =300/>


2. Algorithm was developed to identify these motion in the heading AIS data of ships. 

    - Showing heading variation of ships on map: <img src="heading variation of the ships on map.png"/> you can observe the zig zag motion shown by the ship which was dragging anchor

    - Showing the heading variation profile on time scale <img src="heading variation of the ships.png"/>

3. Algorithm results: 

Ship that was dragging its anchor:

<img src="result1.png"/>

Ship that wasn't dragging its anchor:

<img src="result2.png"/>

A score was defined which is the fraction of zig-zag motion on heading data detected by the algorithm
