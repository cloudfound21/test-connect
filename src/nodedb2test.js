/*require the ibm_db module*/
var ibmdb = require('ibm_db');

console.log("Test program to access DB2 sample database");

/*Connect to the database server
  param 1: The DSN string which has the details of database name to connect to, user id, password, hostname, portnumber 
  param 2: The Callback function to execute when connection attempt to the specified database is completed
*/
ibmdb.open("DRIVER={DB2};DATABASE=sample;UID=username;PWD=password;HOSTNAME=hostname;port=portNumber", function(err, conn)
{
        if(err) {
		/*
		  On error in connection, log the error message on console 
		*/
          	console.error("error: ", err.message);
        } else {

		/*
			On successful connection issue the SQL query by calling the query() function on Database
			param 1: The SQL query to be issued
			param 2: The callback function to execute when the database server responds
		*/
		conn.query("select * from employee fetch first 5 rows only", function(err, employees, moreResultSets) {
                        console.log("FirstName \t\t LastName");
			console.log("----------\t\t---------");

			/*
				Loop through the employees list returned from the select query and print the First name and last name of the employee	
			*/
                        for (var i=0;i<employees.length;i++)
			{
				console.log(employees[i].FIRSTNME, "\t\t", employees[i].LASTNAME);
			}
			console.log("-----------------------");

			/*
				Close the connection to the database
				param 1: The callback function to execute on completion of close function.
			*/
			conn.close(function(){
				console.log("Connection Closed");
			});
		});
	}
});
