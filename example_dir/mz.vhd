

entity mz is
    port (
        clk   : in std_logic;
        reset : in std_logic;
        
    );
end entity mz;

architecture rtl of mz is

begin


    x <= y;


    process (clk)
    begin
        if rising_edge(clk) then
            if reset = '1' then
                
            else
                
            end if;
        end if;
    end process;

    

end architecture;