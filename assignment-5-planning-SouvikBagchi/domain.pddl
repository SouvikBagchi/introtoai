(define (domain sokorobotto)
  (:requirements :typing)
  (:types 
        location - robot-pallete-packing-location
        pallette robot - robot-pallette
        shipment order saleitem - object)
          
 (:predicates 
    (includes ?shipment - shipment ?saleitem - saleitem)
    (orders ?order - order ?saleitem - saleitem)
    (contains ?pallete - pallette ?saleitem - saleitem)
    (at ?robot-pallete - robot-pallette ?location - robot-pallete-packing-location)
    (unstarted ?shipment - shipment)
    (connected ?location ?location - robot-pallete-packing-location)
    (no-robot ?location - robot-pallete-packing-location)
    (no-pallette ?location - robot-pallete-packing-location)
    (available ?location - robot-pallete-packing-location)
    (free ?robot - robot)
    (ships ?shipment - shipment ?order - order)
    (packing-location ?location - robot-pallete-packing-location)
 )
 
 (:action lifting
      :parameters ( ?location - location ?robot - robot   ?pallete - pallette  )
      :precondition (and 
      (at ?pallete ?location)
      (at ?robot ?location)
      (free ?robot)
      )
      :effect (and
      (at ?pallete ?location)
      (at ?robot ?location)
      (not(free ?robot)))
      )
      
      (:action dropping
      :parameters ( ?location - location ?robot - robot  ?pallete - pallette  )
      :precondition (and 
      (at ?pallete ?location)
      (at ?robot ?location)
      (not(free ?robot))
      )
      :effect (and
      (at ?pallete ?location)
      (at ?robot ?location)
      (free ?robot)
      ))
      
    (:action saleitem-load-shipment
      :parameters ( ?pack-location - location ?shipment - shipment ?saleitem -saleitem ?o - order ?robot - robot  ?pallete - pallette)
      :precondition (and 
      (at ?pallete ?pack-location)
      (at ?robot ?pack-location)
      (packing-location ?pack-location)
      (not(free ?robot))
      (contains ?pallete ?saleitem)
      (orders ?o ?saleitem)
      (ships ?shipment ?o)
      (available ?pack-location)
      )
      :effect (and
         (not (contains ?pallete ?saleitem))
         (includes ?shipment ?saleitem)
          )
      )
  
  (:action robot-move-no-pal-location-location
      :parameters (?location1 - location ?location2 - location ?robot1 - robot  )
      :precondition (and 
      (free ?robot1)
      (at ?robot1 ?location1)
      (no-robot ?location2)
      (connected ?location1 ?location2)
      (connected ?location2 ?location1))
      
      
      :effect (and
          (at ?robot1 ?location2 )
          (not(at ?robot1 ?location1))
          (no-robot ?location1)
          (not(at ?robot1 ?location1))
          )
      )
      
      (:action robot-move-with-pal-location-location
      :parameters ( ?location1 - location ?location2 - location ?robot - robot ?pallete - pallette)
      :precondition (and 
      (at ?pallete ?location1 )
      (at ?robot ?location1)
      (no-robot ?location2)
      (connected ?location1 ?location2)
      (connected ?location2 ?location1)
      (no-pallette ?location2))
      
      :effect (and
          (at ?robot  ?location2)
          (at ?pallete  ?location2)
          (no-robot ?location1)
          (no-pallette ?location1)
          (not(at ?pallete ?location1 ))
          (not(at ?robot ?location1)) 
          (not(no-pallette ?location2))
          ))
          
      
      
      
)
