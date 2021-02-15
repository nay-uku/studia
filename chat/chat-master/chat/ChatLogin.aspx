<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="ChatLogin.aspx.cs" Inherits="chat.ChatLogin" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Chat</title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h1>ChatLogin</h1>
            <h3>Menu:</h3>
            <asp:HyperLink ID="HyperLink5" runat="server" NavigateUrl="~/Chat.aspx">Chat</asp:HyperLink><br />
            <asp:HyperLink ID="HyperLink4" runat="server" NavigateUrl="~/ChatLogin.aspx">ChatLogin</asp:HyperLink><br />
        </div>
        <div>
            <asp:TextBox ID="TBlogin" runat="server"></asp:TextBox>
            &nbsp;<asp:Button ID="BtnLogin" runat="server" Text="Zaloguj" OnClick="BtnLogin_Click" />
        </div>
    </form>
</body>
</html>
