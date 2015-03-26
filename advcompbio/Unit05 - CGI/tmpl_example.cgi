
<HTML>
  <HEAD>
    <TITLE>Table</TITLE>
  </HEAD>
  <BODY>
    
    <H4>Table</H4>
    
    <TABLE BORDER=1>
      
      <TR>
        <TD><B>ID</B></TD>
        <TD><B>Length</B></TD>
        <TD><B>Molar Mass</B></TD>
      </TR>
      
      <TMPL_LOOP NAME="sequence_loop">
        <TR>
          <TD><TMPL_VAR NAME="id"></TD>
          <TD><TMPL_VAR NAME="sequence_length"></TD>
          <TD><TMPL_VAR NAME="mm"></TD>
        </TR>
      </TMPL_LOOP>
      
    </TABLE>
    
  </BODY>       
</HTML>
