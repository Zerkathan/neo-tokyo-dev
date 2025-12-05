#!/usr/bin/perl
# Legacy data processing script - CÓDIGO LEGACY DE 2005
# Este script procesa archivos CSV y genera reportes
# TODO: Reescribir esto algún día...

use strict;
use warnings;
use DBI;
use Time::Local;

# Variables globales (mala práctica)
my $DB_HOST = "localhost";
my $DB_USER = "admin";
my $DB_PASS = "password123";
my $LOG_FILE = "/var/log/processor.log";

sub main {
    print "=== DATA PROCESSOR v1.0 ===\n";
    
    # Conectar a DB (sin pool, sin manejo de errores)
    my $dbh = DBI->connect("DBI:mysql:database=company;host=$DB_HOST", 
                           $DB_USER, $DB_PASS)
        or die "Connection failed: $DBI::errstr";
    
    # Procesar archivos (lógica mezclada)
    opendir(my $dh, "./data") or die "Can't open ./data: $!";
    my @files = grep { /\.csv$/ && -f "./data/$_" } readdir($dh);
    closedir $dh;
    
    foreach my $file (@files) {
        print "Processing: $file\n";
        
        # Abrir archivo CSV (sin validación)
        open(my $fh, "<", "./data/$file") or die "Can't open $file: $!";
        
        my $line_count = 0;
        my $total_amount = 0;
        my @errors;
        
        while (my $line = <$fh>) {
            chomp $line;
            $line_count++;
            
            # Saltar header
            next if $line_count == 1;
            
            # Parse CSV (sin biblioteca, vulnerable a edge cases)
            my @fields = split(/,/, $line);
            
            # Validación básica (inconsistente)
            if (@fields < 5) {
                push @errors, "Line $line_count: Not enough fields";
                next;
            }
            
            my ($id, $date, $customer, $amount, $status) = @fields;
            
            # Validar monto (sin manejo de excepciones)
            $amount =~ s/[\$,]//g;  # Quitar $ y comas
            
            # Validar fecha (regex frágil)
            unless ($date =~ /^\d{4}-\d{2}-\d{2}$/) {
                push @errors, "Line $line_count: Invalid date format";
                next;
            }
            
            # Calcular totales (sin verificación de overflow)
            $total_amount += $amount;
            
            # Insertar en DB (SQL injection vulnerable)
            my $query = "INSERT INTO transactions (id, date, customer, amount, status) 
                         VALUES ('$id', '$date', '$customer', $amount, '$status')";
            $dbh->do($query) or print "Error inserting: $DBI::errstr\n";
            
            # Logging mezclado (sin formato consistente)
            if ($amount > 1000) {
                open(my $log, ">>", $LOG_FILE);
                print $log "[ALERT] Large transaction: $id - \$$amount\n";
                close $log;
            }
        }
        
        close $fh;
        
        # Generar reporte (todo en un bloque)
        my $report_file = "./reports/" . $file;
        $report_file =~ s/\.csv$/\_report.txt/;
        
        open(my $report, ">", $report_file) or die "Can't create report: $!";
        print $report "=== REPORT FOR $file ===\n";
        print $report "Total lines: $line_count\n";
        print $report "Total amount: \$$total_amount\n";
        print $report "Errors: " . scalar(@errors) . "\n";
        
        if (@errors) {
            print $report "\nERROR LIST:\n";
            foreach my $err (@errors) {
                print $report "  - $err\n";
            }
        }
        close $report;
        
        print "Report generated: $report_file\n";
    }
    
    $dbh->disconnect();
    print "Processing complete!\n";
}

# Función auxiliar mal ubicada
sub validate_email {
    my ($email) = @_;
    # Regex simplista
    return $email =~ /^[\w\.-]+@[\w\.-]+\.\w+$/;
}

# Función para cleanup (sin usar)
sub cleanup_old_files {
    my ($days) = @_;
    my $cutoff = time() - ($days * 86400);
    # TODO: Implementar esto
}

main();

__END__
Notas del desarrollador original:
- Este script funciona pero es frágil
- No hay tests
- SQL injection vulnerable
- Sin manejo robusto de errores
- Mezcla de responsabilidades
- Hardcoded credentials
- Sin logging estructurado

