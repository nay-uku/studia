<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Chat.aspx.cs" Inherits="chat.Chat" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h1>Chat</h1>
            <h3>Menu:</h3>
            <asp:HyperLink ID="HyperLink5" runat="server" NavigateUrl="~/Chat.aspx">Chat</asp:HyperLink><br />
            <asp:HyperLink ID="HyperLink4" runat="server" NavigateUrl="~/ChatLogin.aspx">ChatLogin</asp:HyperLink><br />
            <br />
        </div>
        <div>
            <asp:GridView ID="GridView1" runat="server" AutoGenerateColumns="False" DataKeyNames="Id" DataSourceID="SqlDataSource1" OnRowDataBound="GridView1_RowDataBound" OnRowCommand="GridView1_RowCommand" OnRowDeleting="GridView1_RowDeleting">
                <Columns>
                    <asp:BoundField DataField="Id" HeaderText="Id" InsertVisible="False" ReadOnly="True" SortExpression="Id" />
                    <asp:BoundField DataField="User" HeaderText="User" SortExpression="User" />
                    <asp:BoundField DataField="Wiadomosc" HeaderText="Wiadomosc" SortExpression="Wiadomosc" />
                    <asp:TemplateField>
                        <ItemTemplate>
                            <asp:Button ID="BtnUsun" CommandArgument='<%# Eval("Id") %>' CommandName="Delete" runat="server" Visible="false" Text="Usun" />
                        </ItemTemplate>
                    </asp:TemplateField>
                </Columns>
            </asp:GridView>
            <asp:SqlDataSource ID="SqlDataSource1" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>" SelectCommand="select * from (select top 5 * from Chat order by Id desc) a order by Id"></asp:SqlDataSource>
            <br />
            <asp:TextBox ID="TBWiad" runat="server" Height="18px" Width="853px"></asp:TextBox>
        </div>
        <p>
            <asp:Button ID="BtnWys" runat="server" Text="Wyslij" OnClick="BtnWys_Click" Visible="false"/>
        </p>
    </form>
</body>
</html>
