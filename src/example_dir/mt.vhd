

entity mt is
    port (
        clk   : in std_logic;
        reset : in std_logic;
    );
end entity mt;

architecture rtl of mt is

begin

    i_mw : entity lib.mw(rtl)
    generic map (
        
    )
    port map (
        
    );

    i_mx : entity lib.mx(rtl)
    generic map (
        
    )
    port map (
        
    );

    i_my : entity lib.my(rtl)
    generic map (
        
    )
    port map (
        
    );

end architecture;