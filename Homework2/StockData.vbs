Attribute VB_Name = "Module1"
Sub StockData()

    'Get all worksheets
    Dim worksheetCount As Integer
    worksheetCount = ActiveWorkbook.Worksheets.Count
    
    'Declare variables
    Dim totalRows As Long
    Dim tickerName As String
    Dim tickerVolume As Double
    Dim totalLocation As Integer
    Dim yearStart As Double
    Dim yearEnd As Double
    Dim percentChange As Double
    'Variables for summary calculations
    Dim greatestVolume As Double
    Dim greatestVolTicker As String
    Dim greatestPercentIncrease As Double
    Dim greatestPITicker As String
    Dim greatestPercentDecrease As Double
    Dim greatestPDTicker As String

    
    For j = 1 To worksheetCount
        'Get total rows in worksheet
        totalRows = ActiveWorkbook.Worksheets(j).Cells(Rows.Count, 1).End(xlUp).Row
        
            
        'Initialize summary variables
        greatestVolume = 0
        greatestPercentIncrease = 0
        greatestPercentDecrease = 0
    
        'Initialize ticker name
        tickerName = ActiveWorkbook.Worksheets(j).Cells(2, 1).Value
    
        'Initialize ticker volume
        tickerVolume = ActiveWorkbook.Worksheets(j).Cells(2, 7).Value
    
        'Set location within worksheet for storing total ticker volume
        totalLocation = 2
        
        'Initialize variable for yearly change
        yearStart = ActiveWorkbook.Worksheets(j).Cells(2, 3).Value
        
        'Set column labels
        ActiveWorkbook.Worksheets(j).Cells(1, 10).Value = "Ticker"
        ActiveWorkbook.Worksheets(j).Cells(1, 11).Value = "Yearly change"
        ActiveWorkbook.Worksheets(j).Cells(1, 12).Value = "Percent change"
        ActiveWorkbook.Worksheets(j).Cells(1, 13).Value = "Total Volume"
        
        'Loop through all rows in the worksheet
        For i = 2 To totalRows
            If ActiveWorkbook.Worksheets(j).Cells(i + 1, 1).Value = tickerName Then
                'We are still looking at the same ticker symbol
                'Count Ticker Volume
                tickerVolume = tickerVolume + ActiveWorkbook.Worksheets(j).Cells(i + 1, 7).Value
            Else
                'We are moving on to a new ticker symbol
                'Get yearEnd value
                yearEnd = ActiveWorkbook.Worksheets(j).Cells(i, 6)
                'Save tickerName, tickerVolume, yearly change
                ActiveWorkbook.Worksheets(j).Cells(totalLocation, 10) = tickerName
                ActiveWorkbook.Worksheets(j).Cells(totalLocation, 13) = tickerVolume
                ActiveWorkbook.Worksheets(j).Cells(totalLocation, 11) = yearEnd - yearStart
                'Color the yearly change based on +/-
                If (yearEnd - yearStart) >= 0 Then
                    ActiveWorkbook.Worksheets(j).Cells(totalLocation, 11).Interior.Color = RGB(0, 255, 0)
                Else
                    ActiveWorkbook.Worksheets(j).Cells(totalLocation, 11).Interior.Color = RGB(255, 0, 0)
                End If
                'Calculate percentage and format cell for percentage value
                If yearStart > 0 Then
                    ActiveWorkbook.Worksheets(j).Cells(totalLocation, 12) = (yearEnd - yearStart) / yearStart
                End If
                ActiveWorkbook.Worksheets(j).Cells(totalLocation, 12).NumberFormat = "0.00%"
                
                'reset yearStart
                yearStart = ActiveWorkbook.Worksheets(j).Cells(i + 1, 3)
                
                'Check for greatest Volume
                If tickerVolume > greatestVolume Then
                    greatestVolume = tickerVolume
                    greatestVolTicker = tickerName
                End If
                'Check for greatest percent increase
                If ActiveWorkbook.Worksheets(j).Cells(totalLocation, 12).Value > greatestPercentIncrease Then
                    greatestPercentIncrease = ActiveWorkbook.Worksheets(j).Cells(totalLocation, 12).Value
                    greatestPITicker = tickerName
                End If
                'Check for greatest percent decrease
                If ActiveWorkbook.Worksheets(j).Cells(totalLocation, 12).Value < greatestPercentDecrease Then
                    greatestPercentDecrease = ActiveWorkbook.Worksheets(j).Cells(totalLocation, 12).Value
                    greatestPDTicker = tickerName
                End If
                'Reset tickerName, tickerVolume and update Location in file to save the next ticker info
                tickerName = ActiveWorkbook.Worksheets(j).Cells(i + 1, 1).Value
                tickerVolume = ActiveWorkbook.Worksheets(j).Cells(i + 1, 7).Value
                totalLocation = totalLocation + 1
            End If
        Next i
    
        'Display Summary
        ActiveWorkbook.Worksheets(j).Range("P1").Value = "Ticker"
        ActiveWorkbook.Worksheets(j).Range("Q1").Value = "Value"
        ActiveWorkbook.Worksheets(j).Range("O2").Value = "Greatest % Increase"
        ActiveWorkbook.Worksheets(j).Range("O3").Value = "Greatest % Decrease"
        ActiveWorkbook.Worksheets(j).Range("O4").Value = "Greatest Total Volume"
        
        ActiveWorkbook.Worksheets(j).Range("P2").Value = greatestPITicker
        ActiveWorkbook.Worksheets(j).Range("Q2").Value = greatestPercentIncrease
        ActiveWorkbook.Worksheets(j).Range("Q2").NumberFormat = "0.00%"
        ActiveWorkbook.Worksheets(j).Range("P3").Value = greatestPDTicker
        ActiveWorkbook.Worksheets(j).Range("Q3").Value = greatestPercentDecrease
        ActiveWorkbook.Worksheets(j).Range("Q3").NumberFormat = "0.00%"
        ActiveWorkbook.Worksheets(j).Range("P4").Value = greatestVolTicker
        ActiveWorkbook.Worksheets(j).Range("Q4").Value = greatestVolume
        
    Next j
    
End Sub

