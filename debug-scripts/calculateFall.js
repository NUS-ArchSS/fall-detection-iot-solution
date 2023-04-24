//Use this function to calculate 
const calculateFall = function (accelX, accelY, accelZ) { 
  pitch = Math.atan2(accelX, Math.sqrt((accelY * accelY) + (accelZ * accelZ))) * 180 / Math.PI;
  roll = Math.atan2(accelY, Math.sqrt((accelX * accelX) + (accelZ * accelZ))) * 180 / Math.PI;  
  
  if((pitch>35)||(pitch<-35)||(roll>35)||(roll<-35)){
	  console.log(pitch +':' + roll + 'Fall detected');
  }else{
	  console.log(pitch +':' + roll + 'No Fall - Normal');
  }
}