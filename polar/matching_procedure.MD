 what we do here:
 
 there are four different treatments for dictators.

  - Baseline - where position is not shown.
  - FR, RB: Forced reveal and reveal_before where position is shown non depending of the wish of the R
  - VL - where position is shown depending on the wish of the R
  
  if we are in the baseline we don't need partner's position
  
  If we in the FL or RB then we need to take into account only the yes and no counters. and values 
  that partner_position may take is either yes or no. 

  If we are in VL then the partner_position can be either yes, no or nr (non-reveal).
  if the total number of Ds matched with Yes exceeds the num_yes, and those matched with No exceeds the num_no,
  then we assign a baseline treatment to the rest. That's to deal with dropouts.
          
The order of treatments is the following:


- We collect Recipients opinion first in VL-R treatment where   after stating their opinion recipients are asked whether they want their opinion to be shown to a dictator.
- Then we conduct two matching Dictators treatments: VL-D first and Baseline-D second. In VL-D we match dictators with one of three types as long as the slots are available. If not, everyone is matched to baseline. Then in baseline we basically don't match because Rs' opinions are not shown.
- When VL-R, VL-D, Baseline-D decisions are taken we match those who are matched in VL-R and the rest we match with whomever we want because they are all baseline.

####THEN the second part starts:

- We conduct baseline-R: the treatment where we do not ask recipients whether they want to reveal their opionion to Ds.
- Then we conduct first FR-D, where we show the participants the Rs' positions. 
- We update the counters and conduct RB-D where Ds can choose whether they want to see the Rs' positions. If counters are exhausted we change their treatments to baseline. 
- Then we match Rs and Ds from Baseline-R to FR-D and RB-D based on their positions.

