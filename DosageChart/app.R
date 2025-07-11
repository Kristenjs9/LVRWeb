library(shiny)
library(tidyverse)
library(DT)
library(readxl)

# UI definition
ui <- fluidPage(
  titlePanel("Dosage Chart Viewer"),
  
    
    mainPanel(
      div(class = "column-screen", style = "padding-left: 10px; padding-right: 10px;",
          h4("Dosage Chart by Animal BW in lbs"),
          DTOutput("dosageTable")
      )
    )
  )


# Server logic
server <- function(input, output, session) {
  # Read and process the dosage data
  dose <- readxl::read_excel("data/Dosage Chart.xlsx") |> 
    mutate(across(where(is.numeric), ceiling))
  
  # Render the datatable
  output$dosageTable <- renderDT({
    datatable(
      dose,
      options = list(
        dom = 't',
        pageLength = nrow(dose),
        paging = FALSE,
        ordering = FALSE,
        drawCallback = JS(
          "function() {
             var table = this.api();
             table.$('td').hover(
               function() {
                 var idx = table.cell(this).index();
                 if (idx) {
                   $(table.row(idx.row).nodes()).addClass('row-highlight');
                   $(table.column(idx.column).nodes()).addClass('col-highlight');
                 }
               },
               function() {
                 var idx = table.cell(this).index();
                 if (idx) {
                   $(table.row(idx.row).nodes()).removeClass('row-highlight');
                   $(table.column(idx.column).nodes()).removeClass('col-highlight');
                 }
               }
             );
             table.columns.adjust(); // Ensure proper alignment
          }"
        )
      ),
      escape = FALSE,
      class = "hover highlight second-table",
      rownames = FALSE
    ) %>% 
      htmlwidgets::onRender("
        function(el) {
          var sheet = document.createElement('style');
          sheet.innerHTML = `
            .second-table thead th {
              font-size: 12px !important;
              font-weight: bold !important;
              padding: 8px !important;
              text-align: center !important;
              background-color: #f9f9f9 !important;
            }
            .second-table tbody td {
              padding: 8px !important;
              text-align: center !important;
              font-size: 12px !important;
            }
            table.dataTable {
              border-collapse: collapse !important;
              width: 100% !important;
            }
            .second-table tbody td:hover {
              outline: 2px solid red !important;
            }
            .second-table .row-highlight {
              background-color: rgba(255, 200, 200, 0.4) !important;
            }
            .second-table .col-highlight {
              background-color: rgba(255, 200, 200, 0.4) !important;
            }
          `;
          document.body.appendChild(sheet);
        }
      ")
  })
}

# Run the application
shinyApp(ui, server)
