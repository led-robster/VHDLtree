

entity my is
    port (
        clk   : in std_logic;
        reset : in std_logic;
        
    );
end entity my;

architecture rtl of my is

begin

    

    i_mz : entity lib.mz(rtl)
    generic map (
        
    )
    port map (
        
    );

    i_mu : entity lib.mu(rtl)
    generic map (
        
    )
    port map (
        
    );

end architecture;