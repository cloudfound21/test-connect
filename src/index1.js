function getSystem() {
var db2Systems = document.querySelectorAll("div.db2System input[name='selector']");
var subSystem;
alert ("subsystem: "+db2Systems);
console.log(db2Systems.length)
for(var i = 0; i < db2Systems.length; i++){
    alert("inside for")
    if(db2Systems[i].checked){
        subSystem = db2Systems[i].labels[0].innerText;
        alert ("subsystem:   "+subSystem);
    }
}


switch (subSystem) {
    case 'DB2C':
      console.log('DB2C selected');
      break;

    case 'DB2X(pre-prod)':
      console.log('DB2X Pre-prod selected');
      break;
      
    case 'DB2X':
    console.log('DB2X selected');
    break;
    
    case 'DB2E':
    console.log('DB2E selected');
    break;
    
  }
}