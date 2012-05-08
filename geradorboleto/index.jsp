<%@ page language="Java" import="boletos.*, java.io.File" %>
<%@page contentType="text/html" %> 

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="pt" lang="pt">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<title>Projeto JSP</title>
	</head>
	<body>
		Este projeto está armazenado na pasta <strong><%= getServletContext().getRealPath("") + System.getProperty( "file.separator" ) %></strong>
		
		<br/><br/><br/>
		<% 
			Boleto bol = new Boleto();
			String teste = bol.teste(); 
			out.print(teste);
		%>
		<br/><br/><br/>

		Os sapinhos fazem hum ah hummmmm!<br/>
		Os sapinhos fazem hum ah hummmmm!<br/>
		Os sapinhos fazem hum ah hummmmm!<br/>
	</body>
</html>