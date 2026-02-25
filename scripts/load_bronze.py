import duckdb
import time
from datetime import datetime

def load_bronze():
    db_path = 'datawarehouse.duckdb'
    base_path = 'datasets' # datasets are in project folder
    
    conn = duckdb.connect(db_path)
    
    try:
        batch_start_time = time.time()
        print('================================================')
        print('Loading Bronze Layer')
        print('================================================')

        # List of tables to load: (Table Name, File Path)
        tables_to_load = [
            # CRM Tables
            ('bronze.crm_cust_info', f'{base_path}/source_crm/cust_info.csv'),
            ('bronze.crm_prd_info', f'{base_path}/source_crm/prd_info.csv'),
            ('bronze.crm_sales_details', f'{base_path}/source_crm/sales_details.csv'),
            # ERP Tables
            ('bronze.erp_loc_a101', f'{base_path}/source_erp/loc_a101.csv'),
            ('bronze.erp_cust_az12', f'{base_path}/source_erp/cust_az12.csv'),
            ('bronze.erp_px_cat_g1v2', f'{base_path}/source_erp/px_cat_g1v2.csv'),
        ]

        for table, file_path in tables_to_load:
            start_time = time.time()
            print(f'>> Truncating Table: {table}')
            conn.execute(f"TRUNCATE TABLE {table};")
            
            print(f'>> Inserting Data Into: {table}')

            conn.execute(f"""
                INSERT INTO {table} 
                SELECT * FROM read_csv('{file_path}', 
                    header=True, 
                    auto_detect=True)
            """)
            record_count = conn.sql(f"SELECT count(*) AS record_count FROM {table}").fetchone()[0]
            print(f'>> Record Count: {record_count}')
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            print(f'>> Load Duration: {duration} seconds')
            print('>> -------------')

        batch_end_time = time.time()
        total_duration = round(batch_end_time - batch_start_time, 2)
        print('==========================================')
        print('Loading Bronze Layer is Completed')
        print(f'   - Total Load Duration: {total_duration} seconds')
        print('==========================================')

    except Exception as e:
        print('==========================================')
        print('ERROR OCCURRED DURING LOADING BRONZE LAYER')
        print(f'Error Message: {str(e)}')
        print('==========================================')
    finally:
        conn.close()

if __name__ == "__main__":
    load_bronze()