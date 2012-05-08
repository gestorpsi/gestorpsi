package boletos;

import java.io.*;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;

import java.util.ArrayList;

public class Boleto
{
	public void Boleto()
	{
	}

	public String teste()
	{
		Connection conn = null;
		Statement stmt = null;
		ResultSet rs = null;
		String database = "gestor";
		String user = "gestor";
		String password = "gestor";

		conn = DriverManager.getConnection("jdbc:mysql://localhost/"+database+"?user="+user+"&password="+password);

		try
		{
	    	String saida = "";
		    stmt = conn.createStatement();
		    if (stmt.execute("SELECT * FROM address_state"))
		    {
		        rs = stmt.getResultSet();
		        while( rs.next() )
		        {
		        	saida += rs.getString("id") + " | ";
		        	saida += rs.getString("name") + " | ";
		        	saida += rs.getString("shortName") + " | ";
		        	saida += rs.getString("country_id") + "\n";
		        }
		    }
		    
		    return saida;
		}
		catch (SQLException ex)
		{
		    return "SQLException: " + ex.getMessage()+"\nSQLState: " + ex.getSQLState()+"\nVendorError: " + ex.getErrorCode();
		}
		finally
		{
	        try
	        {
	        	if( rs != null )
	        		rs.close();
	            rs = null;
	        }
	        catch (SQLException sqlEx) { } // ignore
	        try
	        {
	        	if( stmt != null )
	        		stmt.close();
		        stmt = null;
	        }
	        catch (SQLException sqlEx) { } // ignore
		}
		
		return "fim";
	}

}


