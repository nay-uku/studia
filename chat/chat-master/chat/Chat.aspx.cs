using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data.SqlClient;


namespace chat
{
    public partial class Chat : System.Web.UI.Page
    {
        string user;
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Request.QueryString["login"] != null && Request.QueryString["login"] !="")
            {
                user = Request.QueryString["login"];
                BtnWys.Visible = true;
            }
        }

        protected void BtnWys_Click(object sender, EventArgs e)
        {
            string query = "INSERT INTO Chat " + "Values('" + user + "', '" + TBWiad.Text + "')";
            string connectionString = SqlDataSource1.ConnectionString;
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    connection.Open();
                    command.ExecuteNonQuery();
                    GridView1.DataBind();
                }
            }
        }
        protected void GridView1_RowDataBound(object sender, GridViewRowEventArgs e)
        {
            if (e.Row.RowType != DataControlRowType.DataRow) return;
            {
                //Widzialnosc dla usera
                if (e.Row.Cells[1].Text == user)
                {
                    Button btnUsun = (Button)e.Row.FindControl("btnUsun");
                    btnUsun.Visible = true;
                }
            }
        }
        //Usuniecie
        protected void GridView1_RowCommand(object sender,
                         GridViewCommandEventArgs e)
        {
            if (e.CommandName == "Delete")
            {
                // pobranie id wiersza po kliknieciu na niego
                int ID = Convert.ToInt32(e.CommandArgument);
                // usuniecie
                string query = "DELETE FROM Chat WHERE Id=" + ID;
                string connectionString = SqlDataSource1.ConnectionString;
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    using (SqlCommand command = new SqlCommand(query, connection))
                    {
                        connection.Open();
                        command.ExecuteNonQuery();
                        GridView1.DataBind();
                    }
                }
            }
        }
        protected void GridView1_RowDeleting(object sender, GridViewDeleteEventArgs e)
        {
            Response.Redirect("~/Chat.aspx?login=" + user);
            //ma byc puste - wazne ta metoda musi byc ;/
        }
    }
}